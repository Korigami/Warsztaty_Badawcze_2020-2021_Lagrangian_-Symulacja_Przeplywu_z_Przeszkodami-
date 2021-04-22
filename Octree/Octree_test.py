import octree as ot
import numpy as np
from stl import mesh
#import sys
#np.set_printoptions(threshold=sys.maxsize)

# Ustawienia do siatki krolika
bunny_origin = np.array([30, 30, 30], dtype=np.double)
bunny_r = 90

# Mozna zmieniac, ale wydaje sie optymalne
maximal_leaf_size = 10
maximal_tree_height = 10

path_to_file = 'data/Stanford_Bunny_sample.stl'
bunny_mesh = mesh.Mesh.from_file(path_to_file)

bunny_cube = ot.Cube(bunny_origin, bunny_r)
octree = ot.Octree(bunny_cube, maximal_leaf_size, maximal_tree_height, bunny_mesh)

# Budowa drzewa (mozna podac jako argument liczbe trojkatow, z ktorych chcemy zbudowac drzewo
# np. octree.build(1000) zbuduje drzewo tylko z pierwszych 100 trojkatow) - przydatne do testow
# Brak argumentu oznacza budowe drzewa z wszystkich dostepnych trojkatow
octree.build()

#with open('bunny_octree.txt', 'a') as f:
#    f.write(repr(octree))

# Fejkowe czasteczki
num_of_particles = 5000000
particles = np.array(180*np.random.random_sample((num_of_particles, 3)) - 60, dtype=np.double)

# Macierz trojkatow
found_triangles = octree.search(particles)

#with open('bunny_triangles_matrix.txt', 'a') as f:
#    f.write(repr(found_triangles))

# Przekonwertowana macierz trojaktow (byc moze latwiejsza do wykorzystania niz powyzsza macierz,
# a liczy sie szybko - DO USTALENIA CZY KORZYSTAMY)
converted_found_triangles = ot.convert_found_triangles(found_triangles)

#with open('bunny_triangles_matrix_converted.txt', 'a') as f:
#    f.write(repr(converted_found_triangles))
