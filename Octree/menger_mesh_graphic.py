import octree as ot
import numpy as np
from stl import mesh

menger_origin = np.array([0, 0, 0], dtype=np.double)
menger_r = 2

maximal_leaf_size = 10
maximal_tree_height = 7

path_to_file = 'data/Menger_sponge_sample.stl'
menger_mesh = mesh.Mesh.from_file(path_to_file)

menger_cube = ot.Cube(menger_origin, menger_r)
menger_octree = ot.Octree(menger_cube, maximal_leaf_size, maximal_tree_height, menger_mesh)

menger_octree.build()

plotter = menger_octree.plotter_cubes_mesh()

plotter.show()





