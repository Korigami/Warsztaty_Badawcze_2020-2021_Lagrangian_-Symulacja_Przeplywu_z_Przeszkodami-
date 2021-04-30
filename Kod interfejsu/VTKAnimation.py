import numpy as np
import vtk
from functools import partial

def init_sphere(coords,radius):
    '''
      Create sphere
    '''
    sphere = vtk.vtkSphereSource()
    sphere.SetCenter(coords[0],coords[1],coords[2])
    sphere.SetRadius(radius)
    return sphere

class vtkTimerCallback():
   def __init__(self,actor):
        self.timer_count = 0
        self.actor = actor

   def execute(self,obj,event,param):
        print(self.timer_count)
        if self.timer_count < param.shape[0]:
            self.actor.SetPosition(param[self.timer_count][0], param[self.timer_count][1],param[self.timer_count][2]);
            iren = obj
            iren.GetRenderWindow().Render()
        self.timer_count += 1
    

def add_stl_object(path_to_stl, renderer, colors):
    reader = vtk.vtkSTLReader()
    reader.SetFileName(path_to_stl)

    mapper_stl = vtk.vtkPolyDataMapper()
    mapper_stl.SetInputConnection(reader.GetOutputPort())

    actor_stl = vtk.vtkActor()
    actor_stl.SetMapper(mapper_stl)
    actor_stl.GetProperty().SetDiffuse(0.8)
    actor_stl.GetProperty().SetDiffuseColor(colors.GetColor3d('LightSteelBlue'))
    actor_stl.GetProperty().SetSpecular(0.3)
    actor_stl.GetProperty().SetSpecularPower(60.0)

    renderer.AddActor(actor_stl)

def add_paricles(Coords,renderer,particles_number, colors):
    objects = {i:init_sphere(Coords[i,0,:],10) for i in range(particles_number)}
    mappers = {i:vtk.vtkPolyDataMapper() for i in range(particles_number)}
    actors = {i:vtk.vtkActor() for i in range(particles_number)}
    actors_transformed = dict()
    for i in range(particles_number):
        mappers[i].SetInputConnection(objects[i].GetOutputPort())
        actors[i].SetMapper(mappers[i])
        renderer.AddActor(actors[i])
        actors_transformed[i] = vtkTimerCallback(actors[i])
    return actors_transformed

def prepare_animation(renderer, window, interactor, Coords, particles_number, refresh_rate, path_to_stl):
    colors = vtk.vtkNamedColors()
    
    size = 1000
    window.SetSize(size,size)
    
    renderer.SetBackground(colors.GetColor3d('DarkOliveGreen'))
    
    interactor.GetRenderWindow().AddRenderer(renderer)
    #window.setCentralWidget(interactor)
    
    interactor.GetRenderWindow().GetInteractor().Initialize()

    actors_transformed = add_paricles(Coords, renderer, particles_number, colors)
    add_stl_object(path_to_stl, renderer, colors)
    
    #interactor.SetRenderWindow(window)
    #interactor.Initialize()
    interactor.CreateRepeatingTimer(int(1/refresh_rate))

    # add particles
    for i in range(particles_number):
        interactor.AddObserver("TimerEvent", partial(actors_transformed[i].execute, param=Coords[i,:,:]))

    #timerId = interactor.CreateRepeatingTimer(100) # ???
    #window.Render()
    
    cam = renderer.GetActiveCamera()
    
    position = (5,5,1000)
    zoom = 0.01
    
    cam.SetPosition(position[0],position[1],position[2])
    cam.ParallelProjectionOn()
    cam.Zoom(zoom)
    
    window.Render()
    
    return interactor


