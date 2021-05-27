#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
cimport cython
import numpy as np
cimport numpy as np
import pyvista as pv


cdef np.ndarray[np.double_t,ndim=1] find_min_max(double x0, double x1, double x2):
    """ Funkcja pomocnicza do funkcji Akeine_Moller_triangle_cube_intersection_test() """
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
    """ Funkcja pomocnicza do funkcji Akeine_Moller_triangle_cube_intersection_test() """
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
    """ Test Tomasa Akeine-Mollera na przeciecie trojkata z kostka
        https://fileadmin.cs.lth.se/cs/Personal/Tomas_Akenine-Moller/code
        Przepisane z C do Python
    """

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
        """ Funkcja bazujaca na funkcji Akeine_Moller_triangle_cube_intersection_test
            sprawdza czy nastapilo przeciecie kostki z trojkatem
        """
        cdef np.ndarray[np.double_t,ndim=1] triangle_p1 = triangles_mesh_v0[triangle_idx]
        cdef np.ndarray[np.double_t,ndim=1] triangle_p2 = triangles_mesh_v1[triangle_idx]
        cdef np.ndarray[np.double_t,ndim=1] triangle_p3 = triangles_mesh_v2[triangle_idx]
        cdef np.ndarray[np.double_t,ndim=1] triangle_normal = triangles_mesh_normals[triangle_idx]
        return Akeine_Moller_triangle_cube_intersection_test(self.origin, self.r,
                                                             triangle_p1, triangle_p2, triangle_p3, triangle_normal)

    cdef Cube build_subcube(self, int i, int j, int k):
        """ Funkcja sluzy do podzialu kostki na mniejsze kostki """
        cdef double new_cube_r = self.r/2
        cdef np.ndarray[np.double_t,ndim=1] new_cube_origin = self.origin + (i*new_cube_r, j*new_cube_r, k*new_cube_r)
        return Cube(new_cube_origin, new_cube_r)

    cdef np.ndarray[np.npy_bool,ndim=1] contains_particles(self, np.ndarray[np.double_t,ndim=2] particles):
         """ Funkcja sprawdza czy podane czastki znajduja sie wewnatrz kostki """
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
        """ Funkcja sprawdza czy wierzcholek jest lisciem w drzewie """
        return not self.children

    cdef int is_full(self, int max_leaf_size):
        """ Funkcja sprawdza czy wierzcholek zawiera juz maksymalna liczbe trojkatow """
        return len(self.triangles) >= max_leaf_size

    cdef Node add_child(self, Cube cube):
        """ Funkcja sluzy do przypisywania wierzcholkowi nowego dziecka """
        cdef Node child = Node(cube, self.level+1)
        self.children.append(child)
        return child

    cdef void split(self, np.ndarray[np.double_t,ndim=2] triangles_mesh_v0,
                    np.ndarray[np.double_t,ndim=2] triangles_mesh_v1,
                    np.ndarray[np.double_t,ndim=2] triangles_mesh_v2,
                    np.ndarray[np.double_t,ndim=2] triangles_mesh_normals):
        """ Funkcja sluzy do podzialu wierzcholka """
        cdef int i
        cdef int j
        cdef int k
        cdef Cube subcube
        cdef int new_node_exists
        cdef int triangle_idx
        cdef Node new_node
        # Kazda ponizsza iteracja odpowiada innej mniejszej kostce wzgledem dzielonej kostki
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in [-1, 1]:
                    # Podzial kostki stowarzyszonej z wierzcholkiem na mniejsze kostki
                    curr_subcube = self.cube.build_subcube(i, j, k)
                    self.subcubes.append(curr_subcube)
                    new_node_exists = 0
                    # Iteracja po wszystkich trojkatach przypisanych do dzielonego wierzcholka
                    for triangle_idx in self.triangles:
                        # Sprawdzenie czy trojkat przecina sie z mniejsza kostka
                        if curr_subcube.intersects_triangle(triangle_idx, triangles_mesh_v0,
                                                            triangles_mesh_v1, triangles_mesh_v2, triangles_mesh_normals):
                            # Jesli tak, to wowczas nastepuje sprawdzenie czy wierzcholek stowarzyszony z mniejsza
                            # kostka juz istnieje (taki wierzcholek mogl juz powstac dla innego trojkata)
                            if not new_node_exists:
                                # Jesli nie, to wowczas nastepuje tworzenie nowego wierzcholka (czyli dziecka dla
                                # dzielonego wierzcholka)
                                new_node = self.add_child(curr_subcube)
                                new_node_exists = 1
                            # Przypisanie dziecku trojkata
                            new_node.triangles.append(triangle_idx)
                    # Tworzenie dziecka zwiazanego z mniejsza kostka nastepuje jedynie wowczas gdy do mniejszej kostki
                    # zostal przypisany co najmniej jeden trojkat. Taki zabieg sprawia, ze nie tworza sie niepotrzebnie
                    # puste kostki
                    self.subcubes_node_exists.append(new_node_exists*len(self.children) - 1)
        # Usuniecie wszystkich trojaktow z dzielonego wierzcholka
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
        """ Funkcja zwraca parametry najwiekszej kostki """
        return self.root.cube.r, self.root.cube.origin

    cdef void insert(self, int triangle_idx, Node node=None):
        """ Funkcja sluzy do dodawania nowego trojkata do drzewa poczawszy
            od wierzcholka okreslonego parametrem node
        """
        # Ponizsze wyrazenie logiczne sluzy do obslugi sytuacji gdy trojkat dodawany jest do korzenia (czyli
        # od samego poczatku drzewa)
        if not node:
            if not self.root.is_full(self.max_leaf_size) and self.root.is_leaf():
                self.root.triangles.append(triangle_idx)
            else:
                self.insert(triangle_idx, self.root)

        # Sprawdzenie czy wierzcholek nie jest lisciem
        elif not node.is_leaf():
            # Jesli nie, to wowczas nastepuje dodanie trojkata do dzieci - szczegoly
            # opisane w funkcji add_triangle_to_not_leaf()
            self.add_triangle_to_not_leaf(node, triangle_idx)

        # Jesli wierzcholek jest lisciem, to wowczas nastepuje sprawdzenie czy posiada maksymalna liczbe trojaktow
        elif node.is_full(self.max_leaf_size):
            # Jesli tak, to nastepuje sprawdzenie czy wysokosc wierzcholka jest rowna maksymalnej wysokosci drzewa
            if not node.level == self.max_height:
                # Jesli nie, to nastepuje dzielenie wierzcholka - szczegoly opisane w funkcji split()
                node.split(self.triangles_mesh_v0, self.triangles_mesh_v1, self.triangles_mesh_v2, self.triangles_mesh_normals)
                # Wowczas nastepuje podniesienie wysokosci drzewa o ile wierzcholek byl na samej gorze
                if node.level == self.height:
                    self.height += 1
                # Nastepuje ponowna proba dodania trojkata do wierzcholka (po podzieleniu nie jest juz lisciem)
                self.insert(triangle_idx, node)
            else:
                # Jesli wysokosc wierzcholka jest rowna maksymalnej wysokosci drzewa, to wowczas nie mozna podzielic
                # wierzcholka co skutkuje dodaniem trojkata do wierzcholka mimo przepelnienia trojkatami. Taki zabieg
                # zapobiega rozrastaniu sie drzewa w <nieskonczonosc>
                node.triangles.append(triangle_idx)
                if len(node.triangles) > self.real_max_leaf_size:
                    self.real_max_leaf_size += 1

        else:
            # Jesli wierzcholek jest lisciem, ale nie posiada maksymalnej liczby trojaktow trojaktow, to mozna wowczas
            # dodac kolejny trojkat do wierzcholka
            node.triangles.append(triangle_idx)

    cdef void add_triangle_to_not_leaf(self, Node node, int triangle_idx):
        """ Funkcja dodaje trojkat do wierzcholka niebedacego lisciem """
        cdef int subcube_idx
        cdef Node new_node
        # Ponizsza logika sprawdza czy aby dodac nowy trojkat nalezy stworzyc nowa mniejsza kostke, czy moze
        # ta kostka juz istnieje (wierzcholek zwiazany z ta kostka mogl juz powstac podczas funkcji split())
        # Iteracja po wszystkich mniejszych kostkach
        for subcube_idx in range(len(node.subcubes)):
            # Sprawdzenie czy kostka przecina trojkat
            if node.subcubes[subcube_idx].intersects_triangle(triangle_idx, self.triangles_mesh_v0, self.triangles_mesh_v1,
                                                              self.triangles_mesh_v2, self.triangles_mesh_normals):
                # Jesli tak, to nastepuje sprawdzenie czy wierzcholek zwiazany z ta kostka juz istnieje
                if node.subcubes_node_exists[subcube_idx] > -1:
                    # Jesli tak, to nastepuje dodanie trojkata do tego wierzcholka
                    self.insert(triangle_idx, node.children[node.subcubes_node_exists[subcube_idx]])
                else:
                    # Jesli nie, to nastepuje utworzenie wierzcholka i dodanie do niego trojkata
                    new_node = node.add_child(node.subcubes[subcube_idx])
                    new_node.triangles.append(triangle_idx)
                    node.subcubes_node_exists[subcube_idx] = len(node.children) -1

    cpdef void build(self, int how_many_triangles=-1):
        """ Glowna funkcja pakietu sluzy do budowy drzewa - parametr how_many_triangles okresla z ilu trojkatow
            siatki ma zostac zbudowane drzewo, brak podania parametru skutkuje zbudowaniem drzewa ze wszystkich
            trojkatow
        """
        cdef int triangle_idx
        if how_many_triangles == -1:
            how_many_triangles = len(self.triangles_mesh_v0)
        else:
            how_many_triangles = min(len(self.triangles_mesh_v0), how_many_triangles)
        for triangle_idx in range(how_many_triangles):
            self.insert(triangle_idx)

    cdef np.ndarray[np.int32_t,ndim=2] for_search(self, np.ndarray[np.double_t,ndim=2] particles,
                                              np.ndarray[np.int32_t,ndim=2] triangles, Node node):
        """ Funkcja pomocnicza do funkcji search() sluzy do przeszukiwania drzewa czastkami"""
        # Sprawdzenie czy czastki dotarly do wierzcholka bedacego lisciem
        if node.is_leaf():
            # Jesli tak, to tym czastkom przypisujemy trojkaty ze znalezionego liscia
            triangles[:,:len(node.triangles)] = np.array(node.triangles).astype(np.int)
            return triangles
        cdef Node child
        cdef np.ndarray[np.npy_bool,ndim=1] particles_inside
        # Jesli wierzcholek nie jest lisciem to nastepuje iteracja po wszystkich dzieciach tego wierzcholka
        for child in node.children:
            # Nastepuje wybranie tylko tych czastek sposrod calej macierzy, ktore znajduja sie w kostce zwiazanej
            # z rozwazanym dzieckiem
            particles_inside = child.cube.contains_particles(particles)
            if np.sum(particles_inside) > 0:
                # Nastepuje ponowne przeszukanie wybranych czastek poczawszy od rozwazanego dziecka (taka procedura
                # ostatecznie doprowadzi kazda czastke do pewnego liscia)
                triangles[particles_inside] = self.for_search(particles[particles_inside], triangles[particles_inside], child)
        return triangles

    cpdef np.ndarray[np.int32_t,ndim=2] search(self, np.ndarray[np.double_t,ndim=2] particles):
        """ Glowna funkcja pakietu sluzy do przeszukiwania drzewa czastkami
            - Czastki poza najwieksza kostka otrzymuja wiersz samych wartosci -2
            - Czastki wewnatrz najwiekszej kostki, do ktorych nie zostal przypisany zaden trojkat otrzymuja
              wiersz samych wartosci -1
            - Pozostale czastki otrzymuja w wierszu indeksy przypisanych trojkatow (wartosci -1 nalezy wowczas pominac)
        """
        cdef int row_size_of_triangles = particles.shape[0]
        cdef int column_size_of_triangles = self.real_max_leaf_size
        cdef np.ndarray[np.int32_t,ndim=2] triangles = np.zeros((row_size_of_triangles, column_size_of_triangles), dtype=np.int32) - 2
        cdef np.ndarray[np.npy_bool,ndim=1] particles_inside = self.root.cube.contains_particles(particles)
        triangles[particles_inside] = -1
        triangles[particles_inside] = self.for_search(particles[particles_inside], triangles[particles_inside], self.root)
        return triangles

    cpdef void for_plotter_cubes_mesh(self, Node node, plotter):
        """ Funkcja pomocnicza do funkcji plotter_cubes_mesh() sluzy do graficznego zobrazowania
            zbudowanej siatki kostek
        """
        cdef Node child
        cdef double color_param
        cdef double cube_diam
        cdef double factor = 1/float(self.real_max_leaf_size)
        for child in node.children:
            if child.is_leaf():
                color_param = factor*len(child.triangles)
                cube_diam = 2*child.cube.r
                plotter.add_mesh(pv.Cube(child.cube.origin, cube_diam, cube_diam, cube_diam),
                                 color=[0, color_param, 0])
            self.for_plotter_cubes_mesh(child, plotter)

    def plotter_cubes_mesh(self):
        """ Funkcja sluzy do graficznego zobrazowania zbudowanej siatki kostek """
        plotter = pv.Plotter()
        self.for_plotter_cubes_mesh(self.root, plotter)
        return plotter

    def __repr__(self):
        return 'Height = {}'.format(self.height) + chr(10) + repr(self.root)
