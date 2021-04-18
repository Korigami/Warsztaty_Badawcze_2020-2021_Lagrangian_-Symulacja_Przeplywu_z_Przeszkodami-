import cython
%load_ext cython

%%cython
cimport cython 
import numpy as np
cimport numpy as np
from stl import mesh

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef np.ndarray[np.double_t,ndim=1] find_min_max(double x0, double x1, double x2):
    cdef double p_min = x0
    cdef double p_max = x0
        
    if x1 < p_min:
        p_min = x1
    if x1 > p_max:
        p_max = x1
    if x2 < p_min:
        p_min = x2
    if x2 > p_max:
        p_max = x2
            
    cdef np.ndarray[np.double_t,ndim=1] p = np.array([p_min, p_max], dtype=np.double)
    return p


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef int plane_cube_intersection(np.ndarray[np.double_t,ndim=1] vert, double cube_r, np.ndarray[np.double_t,ndim=1] normal):
    cdef np.ndarray[np.double_t,ndim=1] vmin = np.array([0, 0, 0], dtype=np.double)
    cdef np.ndarray[np.double_t,ndim=1] vmax = np.array([0, 0, 0], dtype=np.double)
    cdef int q
    for q in range(3):
        v = vert[q]
        if normal[q] > 0:
            vmin[q] = -cube_r - v
            vmax[q] = cube_r - v
        else:
            vmin[q] = cube_r - v
            vmax[q] = -cube_r - v
    if np.dot(normal, vmin) > 0:
        return 0
    if np.dot(normal, vmax) >= 0:
        return 1
        
    return 0

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef int Akeine_Moller_triangle_cube_intersection_test(np.ndarray[np.double_t,ndim=1] cube_origin, double cube_r, np.ndarray[np.double_t,ndim=1] triangle_p1,
                                                         np.ndarray[np.double_t,ndim=1] triangle_p2, np.ndarray[np.double_t,ndim=1] triangle_p3, np.ndarray[np.double_t,ndim=1] triangle_normal):
    ### Test Tomasa Akeine-Mollera na przeciecie trojkata z kostka        ###
    ### https://fileadmin.cs.lth.se/cs/Personal/Tomas_Akenine-Moller/code ###
    ### Przepisane z C do Python                                          ###
        
    cdef np.ndarray[np.double_t,ndim=1] v0 = triangle_p1 - cube_origin
    cdef np.ndarray[np.double_t,ndim=1] v1 = triangle_p2 - cube_origin
    cdef np.ndarray[np.double_t,ndim=1] v2 = triangle_p3 - cube_origin
        
    cdef np.ndarray[np.double_t,ndim=1] e0 = v1 - v0
    cdef np.ndarray[np.double_t,ndim=1] e1 = v2 - v1
    cdef np.ndarray[np.double_t,ndim=1] e2 = v0 - v2
    
    ###### Bullet 3 #####
    
    cdef np.ndarray[np.double_t,ndim=1] fe0 = np.abs(e0)
    cdef np.ndarray[np.double_t,ndim=1] fe1 = np.abs(e1)
    cdef np.ndarray[np.double_t,ndim=1] fe2 = np.abs(e2)

    cdef double p0
    cdef double p1
    cdef double p2

    cdef double p_min
    cdef double p_max

    cdef np.ndarray[np.double_t,ndim=1] p

    cdef double rad
        
    #### Test 1 ####
        
    p0 = e0[2]*v0[1] - e0[1]*v0[2]
    p2 = e0[2]*v2[1] - e0[1]*v2[2]
        
    if p0 < p2:
        p_min = p0
        p_max = p2
    else:
        p_min = p2
        p_max = p0
    rad = (fe0[2] + fe0[1])*cube_r
    if p_min > rad or p_max < -rad:
        return 0
  
    #### Test 2 ####
        
    p0 = -e0[2]*v0[0] + e0[0]*v0[2]
    p2 = -e0[2]*v2[0] + e0[0]*v2[2]
        
    if p0 < p2:
        p_min = p0
        p_max = p2
    else:
        p_min = p2
        p_max = p0
    rad = (fe0[2] + fe0[0])*cube_r
    if p_min > rad or p_max < -rad:
        return 0

    #### Test 3 ####
        
    p1 = e0[1]*v1[0] - e0[0]*v1[1]
    p2 = e0[1]*v2[0] - e0[0]*v2[1]
        
    if p2 < p1:
        p_min = p2
        p_max = p1
    else:
        p_min = p1
        p_max = p2
    rad = (fe0[1] + fe0[0])*cube_r
    if p_min > rad or p_max < -rad:
        return 0

    #### Test 4 ####
        
    p0 = e1[2]*v0[1] - e1[1]*v0[2]
    p2 = e1[2]*v2[1] - e1[1]*v2[2]
        
    if p0 < p2:
        p_min = p0
        p_max = p2
    else:
        p_min = p2
        p_max = p0
    rad = (fe1[2] + fe1[1])*cube_r
    if p_min > rad or p_max < -rad:
        return 0

    #### Test 5 ####
        
    p0 = -e1[2]*v0[0] + e1[0]*v0[2]
    p2 = -e1[2]*v2[0] + e1[0]*v2[2]
        
    if p0 < p2:
        p_min = p0
        p_max = p2
    else:
        p_min = p2
        p_max = p0
    rad = (fe1[2] + fe1[0])*cube_r
    if p_min > rad or p_max < -rad:
        return 0

    #### Test 6 ####
        
    p0 = e1[1]*v0[0] - e1[0]*v0[1]
    p1 = e1[1]*v1[0] - e1[0]*v1[1]
        
    if p0 < p1:
        p_min = p0
        p_max = p2
    else:
        p_min = p1
        p_max = p0
    rad = (fe1[1] + fe1[0])*cube_r
    if p_min > rad or p_max < -rad:
        return 0

    #### Test 7 ####
        
    p0 = e2[2]*v0[1] - e2[1]*v0[2]
    p1 = e2[2]*v1[1] - e2[1]*v1[2]
        
    if p0 < p1:
        p_min = p0
        p_max = p1
    else:
        p_min = p1
        p_max = p0
    rad = (fe2[2] + fe2[1])*cube_r
    if p_min > rad or p_max < -rad:
        return 0

    #### Test 8 ####
        
    p0 = -e2[2]*v0[0] + e2[0]*v0[2]
    p1 = -e2[2]*v1[0] + e2[0]*v1[2]
        
    if p0 < p1:
        p_min = p0
        p_max = p1
    else:
        p_min = p1
        p_max = p0
    rad = (fe2[2] + fe2[0])*cube_r
    if p_min > rad or p_max < -rad:
        return 0

    #### Test 9 ####
        
    p1 = e2[1]*v1[0] - e2[0]*v1[1]
    p2 = e2[1]*v2[0] - e2[0]*v2[1]
        
    if p2 < p1:
        p_min = p2
        p_max = p1
    else:
        p_min = p1
        p_max = p2
    rad = (fe2[1] + fe2[0])*cube_r
    if p_min > rad or p_max < -rad:
        return 0

    ##### Bullet 2 ######
    
    ### Test 10 ### 

    p = find_min_max(v0[0], v1[0], v2[0])
    p_min = p[0]
    p_max = p[1]
    
    if p_min > cube_r or p_max < -cube_r:
        return 0

    ### Test 11 ###
    
    p = find_min_max(v0[1], v1[1], v2[1])
    p_min = p[0]
    p_max = p[1]
    
    if p_min > cube_r or p_max < -cube_r:
        return 0

    ### Test 12 ###
    
    p = find_min_max(v0[2], v1[2], v2[2])
    p_min = p[0]
    p_max = p[1]
    
    if p_min > cube_r or p_max < -cube_r:
        return 0

    ##### Bullet 1 ######
    
    ### Test 13 ###
    
    if not plane_cube_intersection(v0, cube_r, triangle_normal):
        return 0

    return 1

class Cube:
            
    def __init__(self, origin, r):
        self.origin = origin
        self.r = r        
        
    def intersects_triangle(self, triangle_idx, triangles_mesh):
        triangle_p1 = triangles_mesh.v0[triangle_idx].astype(np.double)
        triangle_p2 = triangles_mesh.v1[triangle_idx].astype(np.double)
        triangle_p3 = triangles_mesh.v2[triangle_idx].astype(np.double)
        triangle_normal = triangles_mesh.normals[triangle_idx].astype(np.double)
        return Akeine_Moller_triangle_cube_intersection_test(self.origin, self.r,
                                                             triangle_p1, triangle_p2, triangle_p3, triangle_normal)
    
    def build_subcube(self, i, j, k):
        new_cube_r = self.r/2
        new_cube_origin = self.origin + (i*new_cube_r, j*new_cube_r, k*new_cube_r)
        return Cube(new_cube_origin, new_cube_r)
        
    def __repr__(self):
        return 'Origin: {}, r = {}'.format(self.origin, self.r)
    
class Node:
        
    def __init__(self, cube, level):   
        self.triangles = []
        self.children = []
        self.level = level
        self.cube = cube
        self.subcubes = []
        self.subcubes_node_exists = []
        
    def is_leaf(self):
         return not self.children
    
    def is_full(self, max_leaf_size):
          return len(self.triangles) == max_leaf_size
    
    def add_child(self, cube):
        child = Node(cube, self.level+1)
        self.children.append(child)
        return child
        
    def split(self, triangles_mesh):
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in [-1, 1]:
                    curr_subcube = self.cube.build_subcube(i, j, k)
                    self.subcubes.append(curr_subcube)              
                    new_node_exists = False
                    for triangle_idx in self.triangles:  
                        if curr_subcube.intersects_triangle(triangle_idx, triangles_mesh):
                            if not new_node_exists:
                                new_node = self.add_child(curr_subcube)
                                new_node_exists = True
                            new_node.triangles.append(triangle_idx)
                    self.subcubes_node_exists.append(new_node_exists*len(self.children) - 1)
        self.triangles.clear() 
    
    def for_print(self, node, space=1):
        children_str = ''
        for child in node.children:
            children_str += (chr(10) + space*chr(9) + self.for_print(child, space+1))
        return repr(node.cube) + ', level = {}'.format(node.level) + ', triangles = ' + repr(node.triangles) + children_str
            
    def __repr__(self):
        return self.for_print(self)


class Octree:  
            
    
    def __init__(self, init_cube, max_leaf_size, max_height, triangles_mesh):
        self.root = Node(init_cube, 1)
        self.height = 1
        self.max_height = max_height
        self.max_leaf_size = max_leaf_size
        self.triangles_mesh = triangles_mesh
        
    def add_triangle_to_not_leaf(self, node, triangle_idx):
        for subcube_idx in range(len(node.subcubes)):
            if node.subcubes[subcube_idx].intersects_triangle(triangle_idx, self.triangles_mesh):
                if node.subcubes_node_exists[subcube_idx] > -1:
                    self.insert(triangle_idx, node.children[node.subcubes_node_exists[subcube_idx]])
                else:
                    new_node = node.add_child(node.subcubes[subcube_idx])
                    new_node.triangles.append(triangle_idx)   
                    node.subcubes_node_exists[subcube_idx] = len(node.children) -1
    
    def insert(self, triangle_idx, node=None):
        
        if not node:
            if not self.root.is_full(self.max_leaf_size) and self.root.is_leaf():
                self.root.triangles.append(triangle_idx)
            else:
                self.insert(triangle_idx, self.root)
            
        elif not node.is_leaf():
            self.add_triangle_to_not_leaf(node, triangle_idx)
                    
        elif node.is_full(self.max_leaf_size) and not node.level == self.max_height:
            node.split(self.triangles_mesh)
            if node.level == self.height:
                self.height += 1
            self.insert(triangle_idx, node)
            
        else:
            node.triangles.append(triangle_idx)
            
    def build(self):
        for triangle_idx in range(len(self.triangles_mesh.v0)):
            self.insert(triangle_idx)
            
    def __repr__(self):
        return 'Height = {}'.format(self.height) + chr(10) + repr(self.root)  


# Bunny settings
bunny_origin = np.array([30, 30, 30])
bunny_r = 90
maximal_leaf_size = 10
maximal_tree_height = 10
bunny_mesh = mesh.Mesh.from_file('data\Stanford_Bunny_sample.stl')

bunny_cube = Cube(bunny_origin, bunny_r)
octree = Octree(bunny_cube, maximal_leaf_size, maximal_tree_height, bunny_mesh)

octree.build() # Przy tych danych budowa trwa okolo 4 min
# Cython przyspieszyl budowe o rekordowe 5 sekund xDD

print(octree)
