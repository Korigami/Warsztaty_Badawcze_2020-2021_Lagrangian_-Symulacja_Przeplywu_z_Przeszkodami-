import octree as ot
import numpy as np
from stl import mesh
import sys

from Particle import *
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

    path_to_file = 'data/' + mesh_to_load_name + '_sample.stl'
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

    # zainicjujmy czastki
    print("Initiation of particles started!")
    particles = initiate_particles(
        n_part,
        pos_0, vel_0, masses, cross_areas,
        dt
    )
    print("Particles initiated!")
    # zainicjujmy liste wszystkich pozycji czastek
    all_pos = np.ndarray( shape = (n_part, n_time, 3))

    

    for t in range( n_time):

        print( "Wykonano " + str(t) + " z " + str( n_time) + " krokow.")
        # Wyszukajmy z ktorymi trojkatami czastki moga sie zderzyc
        found_triangles = octree.search( cur_positions)
        found_triangles_end = octree.search( new_positions)

        if len( found_triangles_end) != n_part:
            break
    
        # Przechodzimy po czastkach
        for i in range( n_part):

            # Zbieramy obecne pozycje czastek
            all_pos[ i, t, :] = particles[i].cur_pos

            # Zbieramy liste trojkatow z ktorymi moze sie zderzyc nasza czastka
            tr_indexes = found_triangles[i]
            tr_indexes_end = found_triangles_end[i]  

            all_indices = concatenate_list_of_triangles(
                tr_indexes, tr_indexes_end
            )
            n_indices = len( all_indices)

            detected_triangles = np.ndarray( shape = ( n_indices, 5, 3))

            for j in range( n_indices):
                detected_triangles[j] = converted_triangles[ all_indices[ j]]

            # Uaktualniamy pozycje czastek na podstawie wykrytych trojkatow
            particles[i].update_particle_position(
                detected_triangles,
                n_indices,
                0.00001,
                dt
            )
            # Uaktualniamy predkosci czastek na koniec iteracji
            particles[i].update_velocity(
                const,
                dt
            )
        
            # Aktualizujemy pozycje do nastepnej iteracji
            cur_positions[i] = particles[i].cur_pos
            new_positions[i] = particles[i].new_pos
            
    output = open( filename + '.pkl', 'wb')
    pickle.dump( all_pos, output)
    output.close()

    return all_pos