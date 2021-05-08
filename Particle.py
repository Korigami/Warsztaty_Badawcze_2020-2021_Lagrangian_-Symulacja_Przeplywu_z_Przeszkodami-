import numpy as np 
import math

def add_gravity(
    three_vector,
    gravity
):
    return np.array( [ three_vector[0], three_vector[1], three_vector[2] + gravity])

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

    def __init__( self, cur_pos, new_pos, vel, mass, cross_area):
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
        air_friction_constant_part \
            = - constants.fric_coeff * self.cross_area * constants.air_density / 2

        vel_of_part_in_fluid = np.subtract( self.vel, constants.wind_vel)

        air_friction \
            = vel_of_part_in_fluid \
                * math.sqrt( np.dot( vel_of_part_in_fluid, vel_of_part_in_fluid)) * air_friction_constant_part
             

        '''
            Na przyspieszenie składa się siła grawitacji i oporu powietrza
        '''
        acceleration = add_gravity( air_friction, constants.gravity)  # a = (F_g + F_oporu)/m
        acceleration = acceleration * (dt / self.mass)
        
        '''
            Przyspieszenie zmienia się zgodnie z przyspieszneiem
        '''
        self.vel += acceleration # dv = a dt

        
    def get_time_of_hit( 
        self,
        triangle,
        dt
    ):
        # Wysokość nad trójkątem z perspektywy pierwszego wierzchołka
        h_init = np.dot( \
            self.cur_pos - triangle[0],
            triangle[3]    
        )

        # Wysokość pod trójkątem "po przelocie" z perspektywy pierwszego wierzchołka
        h_end = np.dot( \
            self.new_pos - triangle[0],
            triangle[3]
        )

        # Jeśli byliśmy "pod" lub skończyliśmy "nad" trójkątem, to przez niego nie przelecieliśmy
        if h_init < 0 or h_end > 0:
            return np.inf

        hit_time = h_init * dt / (h_init - h_end)
        hit_pos = self.cur_pos + self.vel * hit_time


        mat = np.transpose([ # macierz określa płaszczyznę t0 + a(t1 -t0) + b(t2 -t0)
            triangle[0],
            np.subtract( triangle[1], triangle[0]),
            np.subtract( triangle[2], triangle[0])
        ])

        # Wyrażamy współrzędne punktu zderzenia we wspolrzednych barycentrycznych
        hit_coords = np.linalg.solve( mat, hit_pos) 

        # Aby się zderzyć, musieliśmy wylądować w płaszczyznie t0 + a(t1 -t0) + b(t2 -t0) z warunkami, ze a i b > 0 a ponadto a+b < 1
        # ZMIENIĆ RTOL
        if np.allclose( hit_coords[0], 1, rtol = 1) \
                    and hit_coords[1] > 0  and hit_coords[2] > 0 and hit_coords[1] + hit_coords[2] < 1:
            return hit_time

        else:
            return np.inf 



    def change_part_pos_after_hit(
        self,
        triangle,
        dt 
    ):
        vel_norm_comp = np.dot( self.vel, triangle[3]) # wspolrzedna predkosci do trojkata

        hit_time = self.get_time_of_hit( triangle, dt)

        hit_pos = self.cur_pos + hit_time*self.vel #x(t) = x0 + t*v0

        # Zakladamy odbicia idealnie sprzeyste - przy odbiciu wspolrzedna normalna do powierzchni przechodzi na przeciwna
        self.vel = np.subtract( 
            self.vel,
            2*vel_norm_comp*triangle[3] 
        )

        # Po odbiciu lecimy z nowa predkoscia az do konca iteracji
        self.cur_pos = np.add(
            hit_pos,
            (dt - hit_time)*part.vel
        )
        part.new_pos = part.cur_pos + dt*part.vel #i okreslamy nowa pozycje
        return cur_pos

    def get_full_trajectory(
        self, 
        full_time, dt
    ):
        
        time_steps = full_time // dt 
        trajectory = []

        time_so_far = 0
        while time_so_far < full_time:
            trajectory.append( self.cur_pos)
            self.calc_new_pos( )


#def update_positions_to_all( 
#    particles,
#    dt
#):
