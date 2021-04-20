# Ustawienia do siatki krolika
bunny_origin = np.array([30, 30, 30], dtype=np.double)
bunny_r = 90

# Mozna zmieniac, ale wydaje sie optymalne
maximal_leaf_size = 10
maximal_tree_height = 10

path_to_file = 'Stanford_Bunny_sample.stl'
bunny_mesh = mesh.Mesh.from_file(path_to_file)

bunny_cube = Cube(bunny_origin, bunny_r)
octree = Octree(bunny_cube, maximal_leaf_size, maximal_tree_height, bunny_mesh)

# Budowa drzewa
octree.build()

print(octree)

# Fejkowe czasteczki
num_of_particles = 5000000
particles = np.array(180*np.random.random_sample((num_of_particles,3)) - 60, dtype=np.double)

# Macierz trojkatow
found_triangles = octree.search(particles)

# Przekonwertowana macierz trojaktow (byc moze latwiejsza do wykorzystania niz powyzsza macierz, a liczy sie szybko - DO USTALENIA CZY KORZYSTAMY)
converted_found_triangles = convert_found_triangles(searched_particles)

print(converted_found_triangles)
