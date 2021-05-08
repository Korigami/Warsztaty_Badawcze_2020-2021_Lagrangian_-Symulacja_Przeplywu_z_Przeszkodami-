import numpy as np

class Particle:

    def __init__( self, cur_pos, new_pos, vel, mass, cross_area):
        self.cur_pos = cur_pos
        self.new_pos = new_pos # nowe polozenie jest skladowane, bo jest potrzebne dla kazdego trojkata
        self.vel = vel
        self.mass = mass
        self.cross_area = cross_area

    def update_velocity(
        self,
        constants
    ):
        air_friction_constant_part \
            = constants.fric_coeff * self.cross_area * constants.air_density / 2

        vel_of_part_in_fluid = np.subtract( self.velocity, constants.wind_vel)

        air_friction \
            = (- np.dot( vel_of_part_in_fluid, vel_of_part_in_fluid) * air_friction_constant_part) 
             

class constants:

    def __init__( 
        self,
        grav_const,
        fric_coeff,
        air_density,
        wind_vel,
    ):
        self.grav_const = grav_const
        self.fric_coeff = fric_coeff
        self.air_density = air_density
        self.wind_vel = wind_vel

def get_time_of_hit( 
    part,
    triangle,
    dt
):

    # Wysokość nad trójkątem z perspektywy pierwszego wierzchołka
    h_init = np.dot( 
        part.cur_pos - triangle[0],
        triangle[3]    
    )

    # Wysokość pod trójkątem "po przelocie" z perspektywy pierwszego wierzchołka
    h_end = np.dot(
        part.new_pos - triangle[0],
        triangle[3]
    )

    # Jeśli byliśmy "pod" lub skończyliśmy "nad" trójkątem, to przez niego nie przelecieliśmy
    if h_init < 0 or h_end > 0:
        return np.inf

    hit_time = h_init * dt / (h_init - h_end)
    hit_pos = part.cur_pos + part.vel * hit_time


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
    part,
    triangle,
    hit_time,
    dt 
):
    vel_norm_comp = np.dot( part.vel, triangle[3]) # wspolrzedna predkosci do trojkata

    hit_pos = part.cur_pos + hit_time*part.vel #x(t) = x0 + t*v0

    # Zakladamy odbicia idealnie sprzeyste - przy odbiciu wspolrzedna normalna do powierzchni przechodzi na przeciwna
    part.vel = np.subtract( 
        part.vel,
        2*vel_norm_comp*triangle[3]
    )

    # Po odbiciu lecimy z nowa predkoscia az do konca iteracji
    part.cur_pos = np.add(
        hit_pos,
        (dt - hit_time)*part.vel
    )
    part.new_pos = part.cur_pos + dt*part.vel #i okreslamy nowa pozycje




def calc_new_pos(
    part,
    triangles,
    dt
):
    for triangle in triangles:
        hit_times.append(
            get_time_of_hit(
                part, 
                triangle,
                dt
            )
        )

    hit_time = min( hit_times)
    index_of_hit_triangle = hit_times.index( hit_time)

    change_part_pos_after_hit(
        part, 
        triangles[ index_of_hit_triangle],
        hit_time,
        dt
    )


def update_positions_to_all( 
    particles,
    dt
):
    for particle in particles:
        calc_new_pos(
            particle, 

        )

