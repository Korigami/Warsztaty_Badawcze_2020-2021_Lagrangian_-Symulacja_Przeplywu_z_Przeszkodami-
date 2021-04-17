import numpy as np
import random


class Cube:
    
    def __init__(self, origin, r):
        self.vertices = [origin + (i*r,j*r,k*r) for i in [1, -1] for j in [1, -1] for k in [1, -1]]
        self.origin = origin
        self.r = r
    
    def intersects_triangle(self, triangle):
        return bool(random.getrandbits(1))
        # Do uzupelnienia


class Octree:  
    
    class Node:
        
        def __init__(self, cube):   
            self.triangles = []
            self.children = []
            self.cube = cube
        
        def is_leaf(self):
            return not self.children
    
        def is_full(self, max_leaf_size):
            return len(self.triangles) == max_leaf_size
        
        def split(self):
            for i in [-1, 1]:
                for j in [-1, 1]:
                    for k in [-1, 1]:
                        new_cube_r = node.cube.r/2
                        new_cube_origin = self.cube.origin + (i*new_cube_r, j*new_cube_r, k*new_cube_r)
                        curr_cube = Cube(new_cube_origin, new_cube_r)
                        new_node_exists = False
                        for iter_triangle in self.triangles:  
                            if curr_cube.intersects_triangle(iter_triangle):
                                if not new_node_exists:
                                    new_node = Node(curr_cube)
                                    self.children.append(new_node)
                                    new_node_exists = True
                                new_node.triangles.append(iter_triangle)
            self.triangles.clear()
    
    def __init__(self, init_cube, max_leaf_size):
        self.root = self.Node(init_cube)
        self.max_leaf_size = max_leaf_size
    
    def insert(self, triangle, node=None):
        
        if not node:
            if not self.root.is_full(self.max_leaf_size):
                self.root.triangles.append(triangle)
            else:
                insert(triangle, self.root)
            
        elif not node.is_leaf():
            for child in node.children:
                if child.cube.intersects_triangle(triangle):
                    insert(triangle, child)
                    
        elif node.is_full(self.max_leaf_size):
            node.split()
            insert(triangle, node)
            
        else:
            node.triangles.append(triangle)
    
