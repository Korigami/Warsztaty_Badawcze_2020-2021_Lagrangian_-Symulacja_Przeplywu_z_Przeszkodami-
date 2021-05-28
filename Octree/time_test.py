import octree as ot
import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
import time

bunny_origin = np.array([30, 30, 30], dtype=np.double)
bunny_r = 90
path_to_file = 'data/Stanford_Bunny_sample.stl'
bunny_mesh = mesh.Mesh.from_file(path_to_file)
bunny_cube = ot.Cube(bunny_origin, bunny_r)

build_time = [[], [], []]
search_time = [[], [], []]
height_list = [5, 7, 9, 10]
maximal_leaf_size_list = [10, 20, 50]
num_of_particles = 500000
particles = np.array(180*np.random.random_sample((num_of_particles, 3)) - 60, dtype=np.double)

for idx in range(3):
    for height in height_list:
        maximal_tree_height = height
        bunny_octree = ot.Octree(bunny_cube, maximal_leaf_size_list[idx], maximal_tree_height, bunny_mesh)

        build_start = time.time()
        bunny_octree.build()
        build_end = time.time()
        build_time[idx].append(build_end - build_start)

        search_start = time.time()
        bunny_octree.search(particles)
        search_end = time.time()
        search_time[idx].append(search_end - search_start)


figure, axis = plt.subplots(1, 2)

axis[0].plot(height_list, build_time[0], label='leaf_size=10')
axis[0].plot(height_list, build_time[1], label='leaf_size=20')
axis[0].plot(height_list, build_time[2], label='leaf_size=50')

axis[0].set_title('Czas budowy drzewa')
axis[0].set_xlabel('Wysokosc drzewa')
axis[0].set_ylabel('Czas')

axis[1].plot(height_list, search_time[0], label='leaf_size=10')
axis[1].plot(height_list, search_time[1], label='leaf_size=20')
axis[1].plot(height_list, search_time[2], label='leaf_size=50')

axis[1].set_title('Czas przeszukiwania drzewa')
axis[1].set_xlabel('Wysokosc drzewa')
axis[1].set_ylabel('Czas')

axis[0].legend()
axis[1].legend()

plt.show()

