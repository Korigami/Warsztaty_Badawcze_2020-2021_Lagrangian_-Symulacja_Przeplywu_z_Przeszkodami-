import octree as ot
import numpy as np
from stl import mesh

bunny_origin = np.array([30, 30, 30], dtype=np.double)
bunny_r = 90

maximal_leaf_size = 50
maximal_tree_height = 7

path_to_file = 'data/Stanford_Bunny_sample.stl'
bunny_mesh = mesh.Mesh.from_file(path_to_file)

bunny_cube = ot.Cube(bunny_origin, bunny_r)
bunny_octree = ot.Octree(bunny_cube, maximal_leaf_size, maximal_tree_height, bunny_mesh)

bunny_octree.build()

plotter = bunny_octree.plotter_cubes_mesh()

plotter.show()
