import octree as ot
import numpy as np
from stl import mesh
import sys

from Particle import *
from Triangle import *

import pprint, pickle

from create_matrix_of_positions import *
import numpy as np

filename = "test2" # Podawana bez rozszerzenia
dt = 0.005
n_time = 2000
n_part = 1000
    
pos_0 = np.array( 60*np.random.random_sample((n_part, 3)), dtype=np.double ) 

vel_0 = np.array( [[ 0, 0, -5]] * n_part)

pos_0[:, 2] = 120
    

masses = [0.01] * n_part
cross_areas = [0.01] * n_part
const = Constants( 0.81, 0.04, 0.02, np.array( [0.0, 0.0, 0.0]))
n_triangles = 0

mesh_to_load_name = "Stanford_Bunny"

all_pos = create_matrix_of_all_positions(
    filename, # Podawana bez rozszerzenia
    mesh_to_load_name,
    dt, n_time,
    n_part,
    pos_0, vel_0, masses, cross_areas,
    const,
    n_triangles
)