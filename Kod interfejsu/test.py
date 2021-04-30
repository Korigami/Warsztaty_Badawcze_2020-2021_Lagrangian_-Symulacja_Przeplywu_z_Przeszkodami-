import numpy as np
import vtk
from VTKAnimation import prepare_animation

# Częstotliwość Odświerzania
refresh_rate = 60 # In Hertz

# Ścieżka do stl
#path_to_stl = '../Siatki/Stanford_Bunny_sample.stl'
path_to_stl= '../Siatki/Menger_sponge_sample.stl'

###########  Wygenerowanie danych testowych

particles_number = 20

time_min=0
time_max=100
delta_time=0.1
number_of_time_periods = int((time_max-time_min)//delta_time + 1)


Coords = np.ndarray(shape=(particles_number, number_of_time_periods, 3))

Velocities = np.ndarray(shape=(particles_number, 3))

for i in range(particles_number):
    Velocities[i,0]=np.random.uniform(low=-20,high=20)
    Velocities[i,1]=np.random.uniform(low=-20,high=20)
    Velocities[i,2]=np.random.uniform(low=-2,high=2)

for i in range(particles_number):
    # i-ta cząstka na polu (i,i,0)
    Coords[i,0,0]=np.random.uniform(low=-200,high=200)
    Coords[i,0,1]=np.random.uniform(low=-200,high=200)
    Coords[i,0,2]=np.random.uniform(low=-200,high=200)

for i in range(particles_number):
    for j in range(1,number_of_time_periods):
        for k in range(3):
            Coords[i,j,k]=Coords[i,j-1,k]+Velocities[i,k]*delta_time

if __name__ == "__main__":
    renderer = vtk.vtkRenderer()
    window = vtk.vtkRenderWindow()
    interactor = vtk.vtkRenderWindowInteractor()
    
    interactor = prepare_animation(renderer, window, interactor, Coords, particles_number, refresh_rate,path_to_stl)
    interactor.Start()