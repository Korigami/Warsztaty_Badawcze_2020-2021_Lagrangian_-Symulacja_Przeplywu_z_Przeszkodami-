#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
cimport cython
import numpy as np
cimport numpy as np

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

cpdef int Akeine_Moller_triangle_cube_intersection_test(np.ndarray[np.double_t,ndim=1] cube_origin,
                                                        double cube_r, np.ndarray[np.double_t,ndim=1] triangle_p1,
                                                        np.ndarray[np.double_t,ndim=1] triangle_p2,
                                                        np.ndarray[np.double_t,ndim=1] triangle_p3,
                                                        np.ndarray[np.double_t,ndim=1] triangle_normal):
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


cdef class Cube:
    cdef public:
        origin
        double r

    def __cinit__(self, np.ndarray[np.double_t,ndim=1] origin, double r):
        self.origin = origin
        self.r = r

    cpdef int intersects_triangle(self, int triangle_idx, np.ndarray[np.double_t,ndim=2] triangles_mesh_v0,
                                  np.ndarray[np.double_t,ndim=2] triangles_mesh_v1,
                                  np.ndarray[np.double_t,ndim=2] triangles_mesh_v2,
                                  np.ndarray[np.double_t,ndim=2] triangles_mesh_normals):
        cdef np.ndarray[np.double_t,ndim=1] triangle_p1 = triangles_mesh_v0[triangle_idx]
        cdef np.ndarray[np.double_t,ndim=1] triangle_p2 = triangles_mesh_v1[triangle_idx]
        cdef np.ndarray[np.double_t,ndim=1] triangle_p3 = triangles_mesh_v2[triangle_idx]
        cdef np.ndarray[np.double_t,ndim=1] triangle_normal = triangles_mesh_normals[triangle_idx]
        return Akeine_Moller_triangle_cube_intersection_test(self.origin, self.r,
                                                             triangle_p1, triangle_p2, triangle_p3, triangle_normal)

    cdef Cube build_subcube(self, int i, int j, int k):
        cdef double new_cube_r = self.r/2
        cdef np.ndarray[np.double_t,ndim=1] new_cube_origin = self.origin + (i*new_cube_r, j*new_cube_r, k*new_cube_r)
        return Cube(new_cube_origin, new_cube_r)

    cdef np.ndarray[np.npy_bool,ndim=1] contains_particles(self, np.ndarray[np.double_t,ndim=2] particles):
         return np.sum((self.origin - self.r <= particles) * (particles <= self.origin + self.r), axis=1) == 3

    def __repr__(self):
        return 'Origin: {}, r = {}'.format(self.origin, self.r)


cdef class Node:
    cdef public:
        list triangles
        list children
        int level
        Cube cube
        list subcubes
        list subcubes_node_exists

    def __cinit__(self, Cube cube, int level):
        self.triangles = []
        self.children = []
        self.level = level
        self.cube = cube
        self.subcubes = []
        self.subcubes_node_exists = []

    cdef int is_leaf(self):
        return not self.children

    cdef int is_full(self, int max_leaf_size):
        return len(self.triangles) >= max_leaf_size

    cdef Node add_child(self, Cube cube):
        cdef Node child = Node(cube, self.level+1)
        self.children.append(child)
        return child

    cdef void split(self, np.ndarray[np.double_t,ndim=2] triangles_mesh_v0,
                    np.ndarray[np.double_t,ndim=2] triangles_mesh_v1,
                    np.ndarray[np.double_t,ndim=2] triangles_mesh_v2,
                    np.ndarray[np.double_t,ndim=2] triangles_mesh_normals):
        cdef int i
        cdef int j
        cdef int k
        cdef Cube subcube
        cdef int new_node_exists
        cdef int triangle_idx
        cdef Node new_node
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in [-1, 1]:
                    curr_subcube = self.cube.build_subcube(i, j, k)
                    self.subcubes.append(curr_subcube)
                    new_node_exists = 0
                    for triangle_idx in self.triangles:
                        if curr_subcube.intersects_triangle(triangle_idx, triangles_mesh_v0,
                                                            triangles_mesh_v1, triangles_mesh_v2, triangles_mesh_normals):
                            if not new_node_exists:
                                new_node = self.add_child(curr_subcube)
                                new_node_exists = 1
                            new_node.triangles.append(triangle_idx)
                    self.subcubes_node_exists.append(new_node_exists*len(self.children) - 1)
        self.triangles.clear()

    cdef str for_print(self, Node node, int space=1):
        cdef str children_str = ''
        cdef Node child
        for child in node.children:
            children_str += (chr(10) + space*chr(9) + self.for_print(child, space+1))
        return repr(node.cube) + ', level = {}'.format(node.level) + ', triangles = ' + repr(node.triangles) + children_str

    def __repr__(self):
        return self.for_print(self)

cdef class Octree:
    cdef public:
        Node root
        int height
        int max_height
        int real_max_leaf_size
        int max_leaf_size
        triangles_mesh_v0
        triangles_mesh_v1
        triangles_mesh_v2
        triangles_mesh_normals

    def __cinit__(self, Cube init_cube, int max_leaf_size, int max_height, triangles_mesh):
        self.root = Node(init_cube, 1)
        self.height = 1
        self.max_height = max_height
        self.max_leaf_size = max_leaf_size
        self.real_max_leaf_size = max_leaf_size
        self.triangles_mesh_v0 = triangles_mesh.v0.astype(np.double)
        self.triangles_mesh_v1 = triangles_mesh.v1.astype(np.double)
        self.triangles_mesh_v2 = triangles_mesh.v2.astype(np.double)
        self.triangles_mesh_normals = triangles_mesh.normals.astype(np.double)
        
    cpdef get_biggest_cube_params(self):
        return self.root.cube.r, self.root.cube.origin

    cdef void add_triangle_to_not_leaf(self, Node node, int triangle_idx):
        cdef int subcube_idx
        cdef Node new_node
        for subcube_idx in range(len(node.subcubes)):
            if node.subcubes[subcube_idx].intersects_triangle(triangle_idx, self.triangles_mesh_v0, self.triangles_mesh_v1,
                                                              self.triangles_mesh_v2, self.triangles_mesh_normals):
                if node.subcubes_node_exists[subcube_idx] > -1:
                    self.insert(triangle_idx, node.children[node.subcubes_node_exists[subcube_idx]])
                else:
                    new_node = node.add_child(node.subcubes[subcube_idx])
                    new_node.triangles.append(triangle_idx)
                    node.subcubes_node_exists[subcube_idx] = len(node.children) -1

    cdef void insert(self, int triangle_idx, Node node=None):
        if not node:
            if not self.root.is_full(self.max_leaf_size) and self.root.is_leaf():
                self.root.triangles.append(triangle_idx)
            else:
                self.insert(triangle_idx, self.root)

        elif not node.is_leaf():
            self.add_triangle_to_not_leaf(node, triangle_idx)

        elif node.is_full(self.max_leaf_size):
            if not node.level == self.max_height:
                node.split(self.triangles_mesh_v0, self.triangles_mesh_v1, self.triangles_mesh_v2, self.triangles_mesh_normals)
                if node.level == self.height:
                    self.height += 1
                self.insert(triangle_idx, node)
            else:
                node.triangles.append(triangle_idx)
                if len(node.triangles) > self.real_max_leaf_size:
                    self.real_max_leaf_size += 1

        else:
            node.triangles.append(triangle_idx)

    cpdef void build(self, int how_many_triangles=-1):
        cdef int triangle_idx
        if how_many_triangles == -1:
            how_many_triangles = len(self.triangles_mesh_v0)
        else:
            how_many_triangles = min(len(self.triangles_mesh_v0), how_many_triangles)
        for triangle_idx in range(how_many_triangles):
            self.insert(triangle_idx)

    cdef np.ndarray[np.int32_t,ndim=2] for_search(self, np.ndarray[np.double_t,ndim=2] particles,
                                              np.ndarray[np.int32_t,ndim=2] triangles, Node node):
        if node.is_leaf():
            triangles[:,:len(node.triangles)] = np.array(node.triangles).astype(np.int)
            return triangles
        cdef Node child
        cdef np.ndarray[np.npy_bool,ndim=1] particles_inside
        for child in node.children:
            particles_inside = child.cube.contains_particles(particles)
            if np.sum(particles_inside) > 0:
                triangles[particles_inside] = self.for_search(particles[particles_inside], triangles[particles_inside], child)
        return triangles

    cpdef np.ndarray[np.int32_t,ndim=2] search(self, np.ndarray[np.double_t,ndim=2] particles):
        cdef int row_size_of_triangles = particles.shape[0]
        cdef int column_size_of_triangles = self.real_max_leaf_size
        cdef np.ndarray[np.int32_t,ndim=2] triangles = np.zeros((row_size_of_triangles, column_size_of_triangles), dtype=np.int32) - 2
        cdef np.ndarray[np.npy_bool,ndim=1] particles_inside = self.root.cube.contains_particles(particles)
        triangles[particles_inside] = -1
        triangles[particles_inside] = self.for_search(particles[particles_inside], triangles[particles_inside], self.root) 
        return triangles

    def __repr__(self):
        return 'Height = {}'.format(self.height) + chr(10) + repr(self.root)


def convert_found_triangles(to_convert):
    converted_array = np.zeros((to_convert.shape[0], 2), dtype=object)
    converted_array[:,0] = np.arange(to_convert.shape[0])
    indices_containing_triangles = np.sum(to_convert > -1, axis=1) > 0
    new_to_convert = to_convert.copy()[indices_containing_triangles]
    converted_array = converted_array[indices_containing_triangles]
    triangles_list = []
    for i in range(new_to_convert.shape[0]):
        triangles_list.append(list(new_to_convert[i,:][new_to_convert[i,:] > -1]))
    converted_array[:,1] = triangles_list
    return converted_array
