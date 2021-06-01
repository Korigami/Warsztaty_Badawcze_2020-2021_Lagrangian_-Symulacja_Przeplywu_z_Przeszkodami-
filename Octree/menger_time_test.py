import octree as ot
import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
import time

menger_origin = np.array([0, 0, 0], dtype=np.double)
menger_r = 2
path_to_file = 'data/Menger_sponge_sample.stl'
menger_mesh = mesh.Mesh.from_file(path_to_file)
menger_cube = ot.Cube(menger_origin, menger_r)

build_time = [[], [], [], []]
search_time = [[], [], [], []]
height_list = [5, 7, 9, 10]
maximal_leaf_size_list = [5, 10, 15]
num_of_particles = 500000
particles = np.array(180*np.random.random_sample((num_of_particles, 3)) - 60, dtype=np.double)

for idx in range(3):
    for height in height_list:
        maximal_tree_height = height
        menger_octree = ot.Octree(menger_cube, maximal_leaf_size_list[idx], maximal_tree_height, menger_mesh)

        build_start = time.time()
        menger_octree.build()
        build_end = time.time()
        build_time[idx].append(build_end - build_start)

        search_start = time.time()
        menger_octree.search(particles)
        search_end = time.time()
        search_time[idx].append(search_end - search_start)


figure, axis = plt.subplots(1, 2)
figure.set_size_inches(18.5, 10.5)

axis[0].plot(height_list, build_time[0], label='maximal_leaf_size=5')
axis[0].plot(height_list, build_time[1], label='maximal_leaf_size=10')
axis[0].plot(height_list, build_time[2], label='maximal_leaf_size=15')

axis[0].set_title('Czas budowy drzewa')
axis[0].set_xlabel('Wysokosc drzewa')
axis[0].set_ylabel('Czas')

axis[1].plot(height_list, search_time[0], label='maximal_leaf_size=5')
axis[1].plot(height_list, search_time[1], label='maximal_leaf_size=10')
axis[1].plot(height_list, search_time[2], label='maximal_leaf_size=15')

axis[1].set_title('Czas przeszukiwania drzewa (500 tys. czastek)')
axis[1].set_xlabel('Wysokosc drzewa')
axis[1].set_ylabel('Czas')

axis[0].legend()
axis[1].legend()

plt.show()
