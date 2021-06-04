import numpy as np 
import math

def add_gravity(
    three_vector,
    gravity
):
    return np.array( [ three_vector[0], three_vector[1], three_vector[2] - gravity])

class Constants:

    def __init__( 
        self,
        gravity,
        fric_coeff,
        air_density,
        wind_vel,
    ):
        self.gravity = gravity
        self.fric_coeff = fric_coeff
        self.air_density = air_density
        self.wind_vel = wind_vel


class Particle:

    def __init__( 
        self, 
        cur_pos = np.array([0.0,0.0,0.0]), 
        new_pos = np.array([0.0,0.0,0.0]), 
        vel = np.array([0.0,0.0,0.0]), 
        mass = 0.0, 
        cross_area = 0.0
    ):
        self.cur_pos = cur_pos
        self.new_pos = new_pos # nowe polozenie jest skladowane, bo jest potrzebne dla kazdego trojkata
        self.vel = vel
        self.mass = mass
        self.cross_area = cross_area

    
    def update_velocity(
        self,
        constants,
        dt
    ):
        '''
            Funkcja ma na celu zadanie nowej prędkości czastce po jej przemieszczeniu
            (w tym tez odbiciu).
        '''
        air_friction_constant_part \
            = - constants.fric_coeff \
                * self.cross_area * constants.air_density / 2

        vel_of_part_in_fluid = self.vel - constants.wind_vel

        air_friction \
            = vel_of_part_in_fluid \
                * math.sqrt( 
                    np.dot( 
                        vel_of_part_in_fluid,
                         vel_of_part_in_fluid
                        )
                    ) * air_friction_constant_part
             

        '''
            Na przyspieszenie składa się siła grawitacji i oporu powietrza
        '''
        acceleration = add_gravity( 
            air_friction,
            self.mass * constants.gravity
        )  
        # a = (F_g + F_oporu)/m
        acceleration = acceleration * (dt / self.mass)
        
        '''
            Predkosc zmienia się zgodnie z przyspieszneiem
        '''
        self.vel = self.vel + acceleration # dv = a dt

        # Obliczamy nowa pozycje
        self.new_pos = self.cur_pos + self.vel*dt

    def change_part_pos_after_hit( 
        self,
        triangle, # To jest trojkat jak w Triangle.py, tylko w postaci macierzy 5x3
        hit_time, hit_pos, 
        dt 
    ):

        # wspolrzedna predkosci normalna do trojkata
        vel_norm_comp = \
            np.dot( 
                self.vel,
                triangle[4,]
            )

        # Jesli zderzenie nie zaszlo, to predkosc sie nie zmienia i lecimy przez caly czas
        if hit_time == np.inf:
            self.cur_pos =self.cur_pos + self.vel*dt
            
            return self.cur_pos

        hit_pos = self.cur_pos + hit_time*self.vel #x(t) = x0 + t*v0

        # Zakladamy odbicia idealnie sprezyste - przy odbiciu wspolrzedna normalna do powierzchni przechodzi na przeciwna
        self.vel = self.vel - ( triangle[4,]  * ( 2*vel_norm_comp) )
 

        # Po odbiciu lecimy z nowa predkoscia az do konca iteracji
        self.cur_pos = hit_pos + self.vel * (dt - hit_time)
        

    def update_particle_position(
        self, 
        converted_triangles,
        no_of_triangles,
        tolerance,
        dt
    ):

        # Jezeli nie znalezlismy zadnego trojkata to propagujemy bez zmian
        if no_of_triangles == 0:
            self.cur_pos = self.cur_pos + self.vel * dt 
            return

        # Wysokość nad trójkątem z perspektywy pierwszego wierzchołka
        h_inits = np.einsum( \
            'ij,ij->i',
            self.cur_pos - converted_triangles[:,0,:], # cur_pos - v0
            converted_triangles[:,4,:]
        )
        
        # Wysokość pod trójkątem "po przelocie" z perspektywy pierwszego wierzchołka
        h_ends = np.einsum( \
            'ij,ij->i',
            self.new_pos - converted_triangles[:,0,:], # new_pos - v0
            converted_triangles[:,4,:]
        )

        # Czasy zderzen z plaszczyzna wyznaczona przez trojkaty
        hit_times = np.divide( 
            h_inits * dt,
            h_inits - h_ends
        )
        # Zbieramy miejsca zderzen
        hit_pos = np.outer( hit_times, self.vel) + self.cur_pos

        # Wyrażamy współrzędne punktu zderzenia we wspolrzednych barycentrycznych
        hit_coords = np.einsum( 
            "ijk,ik->ij",
            converted_triangles[:,1:4,:], #A^-1, gdzie A X = hit_pos
            hit_pos
        )

        # Poprawiamy powyzsze czasy o to z ktorej strony sie zderzamy oraz o to,
        # czy trafiamy w trojkat czy poza
        for t in range( no_of_triangles):

            # Gdy zderzenie zaszloze zlej strony
            if h_inits[t] < 0 or h_ends[t] > 0:
                hit_times[t] = np.inf

            # Gdy zderzenie mialo miejsce z dobrej strony
            else:

                # Gdy zderzenie bylo poza trojkatem
                if hit_coords[t,1] < 0 or hit_coords[t, 2] < 0 or hit_coords[t,1] + hit_coords[t,2] > 1:
                    hit_times[t] = np.inf
                
                # Chyba ponizsze niepotrzebne - obliczamy zderzenia z powierzchnia wyznaczona przez trojkat
                #elif not np.allclose( hit_coords[t,0], 1, rtol = tolerance):
                #    hit_times[t] = np.inf

        '''
            W tym momencie hit_times zawiera:
            - jesli zderzenie nie zaszlo, lub zaszlo poza trojkatem:
                np.inf
            - jesli zderzenie zaszlo w trojkacie:
                czas zderzenia
        '''

        # znajdujemy indeks trojkata z ktorym zaszlo zderzenie
        relative_index_of_hit_triangle = hit_times.argmin() 

        # Zmieniamy pozycje czastki po zderzeniu
        self.change_part_pos_after_hit(
            converted_triangles[ relative_index_of_hit_triangle, ],
            hit_times[ relative_index_of_hit_triangle],
            hit_pos[ relative_index_of_hit_triangle],
            dt
        )


    