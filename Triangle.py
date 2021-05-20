import pickle 
import numpy as np

class Triangle:

    def __init__(
        self, 
        v0, v1, v2,
        normal
    ):
        self.v0 = v0 
        self.baricentric_converter_matrix = \
            np.linalg.inv(
                np.transpose(
                    [ 
                        v0,
                        np.subtract( v1, v0),
                        np.subtract( v2, v0)
                    ]
                )
            )
        self.normal = normal / np.linalg.norm( normal)

   
def convert_triangles(
    triangles_v0,
    triangles_v1,
    triangles_v2,
    triangles_normals
):
    no_of_triangles = triangles_v0.shape[0]
    converted_triangles = np.ndarray( shape = (no_of_triangles, 5, 3) )
    
    for t in range( no_of_triangles):

        triangle = Triangle(
                triangles_v0[ t],
                triangles_v1[ t],
                triangles_v2[ t],
                triangles_normals[ t]
            )
        
        converted_triangles[t, 0,] = triangle.v0 
        converted_triangles[t, 1:4,] = triangle.baricentric_converter_matrix
        converted_triangles[t, 4,] = triangle.normal

    return converted_triangles


def save_converted_to_file(
    converted_triangles,
    filename
):

    output = open( filename, 'wb')
    pickle.dump( converted_triangles, output)
    output.close()

def read_converted_from_file(
    filename 
):

    pkl_file = open( filename, 'rb')
    return pickle.load(pkl_file)

def get_converted_triangles(
    all_converted_triangles,
    indices
):
    no_of_triangles = len( indices)
    converted_triangles = np.ndarray( shape = ( no_of_triangles, 5))

    for i in range( no_of_triangles):

        converted_triangles[ i] = all_converted_triangles[ indices[ i]]
        
    return converted_triangles

def concatenate_list_of_triangles(
    list1,
    list2
):
    no_of_valid_in_list1 = list1.argmin()
    no_of_valid_in_list2 = list2.argmin()

    concatenated = np.ndarray( 
        shape = (no_of_valid_in_list1+ no_of_valid_in_list2,),
        dtype = int
    )
    concatenated[:no_of_valid_in_list1] = \
        list1[:no_of_valid_in_list1]

    concatenated[no_of_valid_in_list1:] = \
        list1[:no_of_valid_in_list2]

    return concatenated