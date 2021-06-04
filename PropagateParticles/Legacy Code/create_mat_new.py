import octree as ot
import numpy as np
from stl import mesh
import sys

#from Particle import *
from Triangle import *

import pprint, pickle


def initiate_particles(
    n_particles,
    pos_0, vel_0, masses, cross_areas,
    dt
):
    particles = [ Particle() ] * n_particles

    for p in range( n_particles):
        particles[p] = \
            Particle(
                pos_0[p],
                pos_0[p] + vel_0[p] * dt,
                vel_0[p],
                masses[p],
                cross_areas[p]
            )

    return particles


def create_matrix_of_all_positions(
    filename, # Podawana bez rozszerzenia
    mesh_to_load_name,
    dt, n_time,
    n_part,
    pos_0, vel_0, masses, cross_areas,
    const,
    n_triangles = 0 
):
    # Ustawienia do siatki krolika
    bunny_origin = np.array([30, 30, 30], dtype=np.double)
    bunny_r = 100

    # Mozna zmieniac, ale wydaje sie optymalne
    maximal_leaf_size = 10
    maximal_tree_height = 10

    path_to_file = '/home/kurowskik/VSCode/Python/data/' + mesh_to_load_name + '_sample.stl'
    bunny_mesh = mesh.Mesh.from_file(path_to_file)

    bunny_cube = ot.Cube(bunny_origin, bunny_r)
    octree = ot.Octree(bunny_cube, maximal_leaf_size, maximal_tree_height, bunny_mesh)

    # Budowa drzewa (mozna podac jako argument liczbe trojkatow, z ktorych chcemy zbudowac drzewo
    # np. octree.build(1000) zbuduje drzewo tylko z pierwszych 100 trojkatow) - przydatne do testow
    # Brak argumentu oznacza budowe drzewa z wszystkich dostepnych trojkatow

    print("Creation of mesh started!")
    if n_triangles == 0:
        octree.build( )
    else:
        octree.build( n_triangles)

    print("Mesh created!")

    cur_positions = pos_0 
    new_positions = pos_0 + vel_0 * dt

    # Przekonwertujmy czastki aby szybciej liczyc
    print("Conversion of triangles started!")
    converted_triangles = convert_triangles(
        octree.triangles_mesh_v0,
        octree.triangles_mesh_v1,
        octree.triangles_mesh_v2,
        octree.triangles_mesh_normals
    )
    print("Triangles converted!")

    n_triangles = converted_triangles.shape[0]

    ## zainicjujmy czastki
    #print("Initiation of particles started!")
    #particles = initiate_particles(
    #    n_part,
    #    pos_0, vel_0, masses, cross_areas,
    #    dt
    #)
    print("Particles initiated!")
    # zainicjujmy liste wszystkich pozycji czastek
    all_pos = np.ndarray( shape = (n_part, n_time+2, 3)) # +2 bo nowe nowe

    cur_poses = pos_0.copy()

    all_pos[:,0,:] = pos_0
    all_pos[:,1,:] = pos_0 + vel_0 * dt

    #vels = v0.copy()
    #mases
    #cross_areas

    # n_detected to 2x wymiar drugi octree.search   
    n_detected = 20

    detected_triangles = np.ndarray( shape = (n_detected, n_part, 5, 3))

    arange = np.arange( n_part)
    inv_masses = 1/masses


    for t in range( n_time):

        print( "Wykonano " + str(t) + " z " + str( n_time) + " krokow.")

        '''
            ZNAJDYWANIE TRÓJKĄTÓW DO POTENCJALNEGO ZDERZENIA

            Wybieramy te trójkąty, które znajdują się w tym samym sześcianie
            co cząstka w pozycji początkowej i końcowej swojego ruchu.
            (Zakładamy tu, że cząstka może przemieścić się o co najwyżej jeden sześcian.)
        '''
        det_triangles_indeces = np.concatenate(
            [
                octree.search( all_pos[:,t,:]),
                octree.search( all_pos[:,t+1,:])
            ],
            axis = 1
        ).transpose()
        detected_triangles = converted_triangles[ det_triangles_indeces]


        maximal_indeces_of_detected_triangles = np.amax( det_triangles_indeces, axis = 1)

        '''
            POZYCJA POCZĄTKOWA I KOŃCOWA NAD TRÓJKĄTEM:

            Poniżej znajdujemy wysokości cząstek nad trójkątami w pozycji początkowej 
            i końcowej.
        '''
        # Pozycje początkowe
        h_inits = np.einsum( \
            'tpx,tpx->pt',
            all_pos[:,t,:] - detected_triangles[:,:,0,:], # cur_pos - v0
            detected_triangles[:,:,4,:]
        )
        # Pozycje końcowe
        h_ends = np.einsum( \
            'tpx,tpx->pt',
            all_pos[:,t+1,:] - detected_triangles[:,:,0,:], # new_pos - v0
            detected_triangles[:,:,4,:]
        )

        '''
            CZASY I MIEJSCA ZDERZEN:

            Poniżej obliczamy czasy i miejsca zderzeń z płaszczyzną generowaną
            przez każdy z trójkątów będących kandydatami do zderzenia.
            Wyrażamy następnie punkty tych zderzenia we współrzędnych
            barycentrycznych względem każdego z trójkątów.
        '''
        # Czasy zderzen z plaszczyzna wyznaczona przez trojkaty
        hit_times = np.divide( 
            h_inits * dt,
            h_inits - h_ends
        )
        # Zbieramy miejsca zderzen
        hit_pos = np.einsum(
            'pt,px->tpx',
            hit_times, vel_0
        ) + all_pos[:,t,:]
        # Wyrażamy współrzędne punktu zderzenia we wspolrzednych barycentrycznych
        hit_coords = np.einsum( 
            "tpjk,tpk->ptj",
            detected_triangles[:,:,1:4,:], #A^-1, gdzie A X = hit_pos
            hit_pos
        )

        '''
            WARUNKI NA ZDERZENIE
            - zderzenie zaszło w czasie [0, dt]
            - zderzenie zaszło od strony zewnętrznej
            - zderzenie zaszło wenwątrz trójkąta 

            jeżeli nie są spełnione, to zderzenie nie zaszło (stąd np.inf)
        '''
        # zderzenie zaszło w czasie [0, dt]
        hit_times[ hit_times > dt ] = np.inf
        hit_times[ hit_times < 0] = np.inf
        # zderzenie zaszło od strony zewnętrznej
        hit_times[ h_inits < 0 ] = np.inf
        hit_times[ h_ends > 0 ] = np.inf
        # zderzenie zaszło wenwątrz trójkąta 
        hit_times[ hit_coords[:,:,1] < 0 ] = np.inf
        hit_times[ hit_coords[:,:, 2] < 0 ] = np.inf
        hit_times[ hit_coords[:,:,1] + hit_coords[:,:,2] > 1  ] = np.inf


        '''
            UZYSKIWANIE NAJLEPSZYCH KANDYDATÓW NA ZDERZENIE:

            Najlepszymi kandydatami na zderzenie są trójkąty z najmniejszym (dodatnim)
            czasem zderzenia. Wybieramy zatem trójkąt odpowiadający najktószemu 
            czasowi do zderzenia.
        '''
        relative_index_of_hit_triangle = np.argmin( hit_times, axis=1)
        true_hit_times = np.amin( hit_times, axis = 1)
        hit_triangles = detected_triangles[ relative_index_of_hit_triangle, arange]

        


        vel_norm_comp = \
            np.einsum(
                'px,px->p',
                vel_0,
                hit_triangles[:,4,:]
            )

        hit_pos = all_pos[:,t,:] + np.einsum(
            'p,px->px',
            true_hit_times,
            vel_0 
        )

        vel_0[ true_hit_times != np.inf] = \
            vel_0[ true_hit_times != np.inf] - np.einsum(
            'px,p->px',
            hit_triangles[ true_hit_times != np.inf][:,4,:],
            2*vel_norm_comp[ true_hit_times != np.inf]
        )   

        all_pos[ true_hit_times != np.inf][:,t+1,:] = hit_pos[ true_hit_times != np.inf] + np.einsum(
            'px,p->px',
            vel_0[ true_hit_times != np.inf],
            dt - true_hit_times[ true_hit_times != np.inf]     
        )
        
        all_pos[:,t+1,:][ true_hit_times  == np.inf] = \
            all_pos[:,t,:][ true_hit_times  == np.inf] + vel_0[ true_hit_times  == np.inf]*dt


        '''
            Funkcja ma na celu zadanie nowej prędkości czastce po jej przemieszczeniu
            (w tym tez odbiciu).
        '''
        air_friction_constant_part \
            = cross_areas * (- const.fric_coeff * const.air_density / 2)

        vel_of_part_in_fluid = vel_0 - const.wind_vel

        air_friction \
            = np.einsum(
                'px,p->px',
                vel_of_part_in_fluid,
                np.linalg.norm(
                    vel_of_part_in_fluid,
                    axis = 1
                ) * air_friction_constant_part
            ) 

        air_friction_acc = np.einsum( 
            'px,p->px',
            air_friction,
            inv_masses 
        )
        acc = air_friction_acc + const.gravity

        '''
            Na przyspieszenie składa się siła grawitacji i oporu powietrza
        '''
        #acceleration = add_gravity( 
        #    air_friction,
        #    self.mass * constants.gravity
        #)  
        # a = (F_g + F_oporu)/m
        #acceleration = np.einsum(
        #    'px,p->px',
        #    acceleration *dt,
        #    1/masses)
        
        '''
            Predkosc zmienia się zgodnie z przyspieszneiem
        '''
        vel_0 = vel_0 + acc*dt
        #self.vel = self.vel + acceleration # dv = a dt
        all_pos[:,t+2,:] = all_pos[:,t+1,:] + vel_0*dt

            
    output = open( filename + '.pkl', 'wb')
    pickle.dump( all_pos, output)
    output.close()

    return all_pos