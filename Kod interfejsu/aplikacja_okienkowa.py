import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import Qt, QtCore, QtGui, QtWidgets

import numpy as np 
import sys, time

import pyvista as pv

import pandas as pd

# STAŁE PARAMETRY
path_to_stl = '../Siatki/'
stl_files = {'Krolik':path_to_stl+'Stanford_Bunny_sample.stl', 
             'Kostka Mengera' : path_to_stl+'Menger_sponge_sample.stl',
             'Kostka': path_to_stl+'Cube_3d_printing_sample.stl'}


###################################
######  APLIKACJA OKIENKOWA  ######
###################################
class BaseWindow(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(20, 20, 400, 100)
        self.setWindowTitle("NAZWA APKI")
        self.center()

    def center(self):
        frameGm = self.frameGeometry()
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


class StartWindow(BaseWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interfejs()
        self.show()

    def interfejs(self):
        ukladT = QGridLayout()
        
        Info = QLabel("Jakaś informacja", self)
        ukladT.addWidget(Info, 0, 0)
        
        ukladH1 = QHBoxLayout()
        self.vizualizeBtn = QPushButton("&Wizualizacja", self)
        self.vizualizeBtn.clicked.connect(self.switch_vizualize_window)
        ukladH1.addWidget(self.vizualizeBtn)
        ukladT.addLayout(ukladH1, 1, 0, 1, 3)

        ukladH2 = QHBoxLayout()
        self.authorsBtn = QPushButton("&Autorzy", self)
        self.authorsBtn.clicked.connect(self.switch_authors_window)
        ukladH2.addWidget(self.authorsBtn)
        ukladT.addLayout(ukladH2, 2, 0, 1, 3)
    
        self.setLayout(ukladT)
        
    @pyqtSlot()
    def switch_vizualize_window(self):
        self.cams = VizualizeWindow() 
        self.cams.show()
        self.close()

    @pyqtSlot()
    def switch_authors_window(self):
        self.cams = AuthorsWindow() 
        self.cams.show()
        self.close()
    

class VizualizeWindow(BaseWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interfejs()
        self.show()

    def choose_object(self,ukladT):
        
        InfoObject = QLabel("wybierz obiekt", self)
        ukladT.addWidget(InfoObject, 0, 0)
        
        self.Object = QListWidget(self)
        self.Object.setGeometry(50, 70, 100, 60)
        item1 = QListWidgetItem("Krolik")
        item2 = QListWidgetItem("Kostka")
        item3 = QListWidgetItem("Kostka Mengera")
        self.Object.addItem(item1)
        self.Object.addItem(item2)
        self.Object.addItem(item3)
        ukladT.addWidget(self.Object, 1, 0)
        
    def choose_partcles_number(self,ukladT):
        InfoParticlesNumber = QLabel("podaj liczbę cząsteczek", self)
        ukladT.addWidget(InfoParticlesNumber, 2, 0)
        
        self.particles_number = QSpinBox()
        self.particles_number.setMinimum(0)
        self.particles_number.setMaximum(50)
        self.particles_number.setValue(20)
        ukladT.addWidget(self.particles_number, 3, 0)
    
    def choose_number_of_time_periods(self,ukladT):
        InfoTimeMax = QLabel("Podaj liczbę iteracji", self)
        ukladT.addWidget(InfoTimeMax, 4, 0)
        
        self.number_of_time_periods = QSpinBox()
        self.number_of_time_periods.setMinimum(1)
        self.number_of_time_periods.setMaximum(100)
        self.number_of_time_periods.setValue(50)
        ukladT.addWidget(self.number_of_time_periods, 5, 0)
    
    def choose_delta_time(self,ukladT):
        InfoDeltaTime = QLabel("Podaj krok czasowy (w ms).", self)
        ukladT.addWidget(InfoDeltaTime, 6, 0)
        
        self.delta_time = QSpinBox()
        self.delta_time.setMinimum(10)
        self.delta_time.setMaximum(1000)
        self.delta_time.setValue(500)
        ukladT.addWidget(self.delta_time, 7, 0)
    
    def btnstate(self,b):
        if b.isChecked() == True:
            self.save = b.text()
        
    def choose_if_save(self,ukladT):
        
        InfoObject = QLabel("Czy chcesz zapisać animację w formacie Gif/Avi?", self)
        ukladT.addWidget(InfoObject, 8, 0)
        
        layout = QHBoxLayout()
        
        self.b1 = QRadioButton("Nie")
        self.b1.setChecked(True)
        self.save = "Nie"
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        layout.addWidget(self.b1)
        
        self.b2 = QRadioButton("Gif")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))
        layout.addWidget(self.b2)
        
        self.b3 = QRadioButton("Avi")
        self.b3.toggled.connect(lambda:self.btnstate(self.b3))
        layout.addWidget(self.b3)
        
        ukladT.addLayout(layout, 9, 0)
        
    def interfejs(self):
        ukladT = QGridLayout()
        
        self.choose_object(ukladT)  # Wybór obiektu
        self.choose_partcles_number(ukladT) # Wybór liczby cząsteczek
        self.choose_number_of_time_periods(ukladT) # Liczba iteracji
        self.choose_delta_time(ukladT) # Podaj krok czasowy
        self.choose_if_save(ukladT) # Czy zapisujemy
        
        ##### Przycisk Ok
        ukladH = QHBoxLayout()
        self.OkBtn = QPushButton("&OK", self)
        self.OkBtn.clicked.connect(self.switch_result_window)
        ukladH.addWidget(self.OkBtn)
        ukladT.addLayout(ukladH, 10, 0)
        ########
        
        self.setLayout(ukladT)
    
    #####################################################################3
    # def Tmp_Simulation(self,particles_number,number_of_time_periods,delta_time):
    #     Coords = np.ndarray(shape=(particles_number, number_of_time_periods, 3))

    #     Velocities = np.ndarray(shape=(particles_number, 3))

    #     for i in range(particles_number):
    #         Velocities[i,0]=np.random.uniform(low=-20,high=20)
    #         Velocities[i,1]=np.random.uniform(low=-20,high=20)
    #         Velocities[i,2]=np.random.uniform(low=-2,high=2)

    #     for i in range(particles_number):
    #         #i-ta cząstka na polu (i,i,0)
    #         Coords[i,0,0]=np.random.uniform(low=-200,high=200)
    #         Coords[i,0,1]=np.random.uniform(low=-200,high=200)
    #         Coords[i,0,2]=np.random.uniform(low=-200,high=200)

    #     for i in range(particles_number):
    #         for j in range(1,number_of_time_periods):
    #             for k in range(3):
    #                 Coords[i,j,k]=Coords[i,j-1,k]+Velocities[i,k]*delta_time/1000
    #     return Coords
    #####################################################################3
    
    def Tmp_Simulation(self,particles_number,number_of_time_periods,delta_time):
        self.particles_number = 25
        self.number_of_time_periods = 100
        Coords = pd.read_pickle('positions6.pkl')
        return Coords
    
    
    def Calculations(self):
        save = self.save
        particles_number = self.particles_number.value()
        number_of_time_periods = self.number_of_time_periods.value()
        Object = self.Object.currentItem().text()
        delta_time = self.delta_time.value()
        
        #### Tutaj wyznaczanie coords
        Coords = self.Tmp_Simulation(particles_number,number_of_time_periods,delta_time)
        ####
        
        return particles_number, number_of_time_periods, Object, Coords, save
        
    
    @pyqtSlot()
    def switch_result_window(self):
        self.cams = ResultWindow(self.Calculations())
        self.cams.show()
        self.close() 
    

class AuthorsWindow(BaseWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interfejs()
        self.show()
    
    # metoda tej klasy
    def interfejs(self):
        ukladT = QGridLayout()
        
        Info1 = QLabel("Autorzy:", self)
        ukladT.addWidget(Info1, 0, 0)
        
        Info2 = QLabel(" 1) Paweł Lefelbajn", self)
        ukladT.addWidget(Info2, 1, 0)
        
        Info3 = QLabel(" 2) Michał Dybowski", self)
        ukladT.addWidget(Info3, 2, 0)
        
        Info4 = QLabel(" 3) Kacper Kurowski", self)
        ukladT.addWidget(Info4, 3, 0)     
        
        self.returnBtn = QPushButton("&Powrót", self)
        self.returnBtn.clicked.connect(self.switch_start_window)
        ukladH1 = QHBoxLayout()
        ukladH1.addWidget(self.returnBtn)
        ukladT.addLayout(ukladH1, 4, 0)
        
        self.setLayout(ukladT)
        
    @pyqtSlot()
    def switch_start_window(self):
        self.cams = StartWindow() 
        self.cams.show()
        self.close()
    

class ResultWindow(BaseWindow):
    def __init__(self, args, parent=None): 
        super().__init__(parent)       
        self.interfejs(args)
        self.show()

    def single_animation(self, particles_number, j, Object, Coords, save):
        for i in range(particles_number):
            self.plotter.add_mesh(
                    pv.Sphere(
                        radius = 0.4,
                        center = (
                            Coords[i,j,0],
                            Coords[i,j,1],
                            Coords[i,j,2]
                            )
                    ),
                    name = f"{i}",
                    smooth_shading=True,
                    color = 'red'
                    )
                        
    def animate(self,particles_number, number_of_time_periods ,Object, Coords, save):
        if save == "Avi":
            self.plotter.open_movie(f"{Object}.avi",framerate = 10)
        elif save == "Gif":
            self.plotter.open_gif(f"{Object}.gif")
        for j in range(number_of_time_periods):
            start_time = time.time()
            self.single_animation(particles_number, j, Object, Coords, save)
            if save != "Nie":
                self.plotter.write_frame()
            print("--- %s seconds ---" % (time.time() - start_time))
        self.plotter.close()
        
    def interfejs(self,args):
        ukladT = QGridLayout()
        # etykiety
        particles_number = args[0]
        number_of_time_periods = args[1]
        Object = args[2]
        Coords = args[3]
        save = args[4]
        # print(particles_number)
        # print(number_of_time_periods)
        # print(Object)
        # print(save)
        
        self.plotter = pv.Plotter(window_size=[1920,1080])#,line_smoothing =True, point_smoothing= True, polygon_smoothing = True)
        self.plotter.set_background(color='white')
        self.mesh = pv.PolyData(path_to_stl+stl_files[Object])
        self.plotter.add_mesh(self.mesh ,name = f"{Object}", color = 'green')
        self.plotter.show(auto_close=False)
        
        self.animate(particles_number,
                    number_of_time_periods,
                    Object,
                    Coords, 
                    save)
        
        self.returnbtn = QPushButton("&Zamknij", self)
        self.returnbtn.clicked.connect(self.zamknij)

        ukladH1 = QHBoxLayout()
        ukladH1.addWidget(self.returnbtn)

        ukladT.addLayout(ukladH1, 1, 0, 1, 3)
        self.setLayout(ukladT)
        
    @pyqtSlot()
    def zamknij(self):
        self.plotter.close()
        self.close()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = StartWindow()
    sys.exit(app.exec_())

