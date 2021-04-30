import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import Qt, QtCore, QtGui

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

import numpy as np 
import sys

from VTKAnimation import prepare_animation


###############################
######  PRZYKŁADOWE DANE ######
###############################


# STAŁE PARAMETRY

path_to_stl = '../Siatki/'
stl_files = {'Krolik':path_to_stl+'Stanford_Bunny_sample.stl', 
             'Kostka Mengera' : path_to_stl+'Menger_sponge_sample.stl',
             'Kostka': path_to_stl+'Cube_3d_printing_sample.stl'}
time_min=0 

########### zmienne
# Częstotliwość Odświeżania
refresh_rate = 60 # In Hertz

particles_number = 20

time_max=100
delta_time=0.1
           

###################################
######  APLIKACJA OKIENKOWA  ######
###################################


class StartWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interfejs()

    def center(self):
        frameGm = self.frameGeometry()
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    
    def interfejs(self):
        # etykiety
        Info = QLabel("Wybierz obiekt", self)
        ukladT = QGridLayout()
        ukladT.addWidget(Info, 0, 0)

        self.vizualizeBtn = QPushButton("&Wizualizacja", self)
        self.vizualizeBtn.clicked.connect(self.switch_vizualize_window)

        self.authorsBtn = QPushButton("&Autorzy", self)
        self.authorsBtn.clicked.connect(self.switch_authors_window)

        ukladH1 = QHBoxLayout()
        ukladH1.addWidget(self.vizualizeBtn)

        ukladH2 = QHBoxLayout()
        ukladH2.addWidget(self.authorsBtn)

        # przypisanie utworzonego układu do okna
        self.setLayout(ukladT)
        ukladT.addLayout(ukladH1, 1, 0, 1, 3)
        ukladT.addLayout(ukladH2, 2, 0, 1, 3)
        
        self.setGeometry(20, 20, 400, 100)
        self.setWindowTitle("NAZWA APKI")
        self.center()
        self.show()

    
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
    
    

class VizualizeWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()

    def center(self):
        frameGm = self.frameGeometry()
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def interfejs(self):
        # etykiety
        ukladT = QGridLayout()
        
        
        # Wybór obiektu
        self.Object = QListWidget(self)
        self.Object.setGeometry(50, 70, 100, 60)
        item1 = QListWidgetItem("Krolik")
        item2 = QListWidgetItem("Kostka")
        item3 = QListWidgetItem("Kostka Mengera")
        self.Object.addItem(item1)
        self.Object.addItem(item2)
        self.Object.addItem(item3)
        InfoObject = QLabel("wybierz obiekt", self)
        ukladT.addWidget(InfoObject, 0, 0)
        ukladT.addWidget(self.Object, 1, 0)
    
        # Wybór liczby cząsteczek
        self.particles_number = QSpinBox()
        self.particles_number.setMinimum(0)
        self.particles_number.setMaximum(50)
        self.particles_number.setValue(20)
        InfoParticlesNumber = QLabel("podaj liczbę cząsteczek", self)
        ukladT.addWidget(InfoParticlesNumber, 2, 0)
        ukladT.addWidget(self.particles_number, 3, 0)
        
        # Czas końcowy
        self.time_max = QSpinBox()
        self.time_max.setMinimum(1)
        self.time_max.setMaximum(100)
        self.time_max.setValue(50)
        InfoTimeMax = QLabel("podaj czas końcowy", self)
        ukladT.addWidget(InfoTimeMax, 4, 0)
        ukladT.addWidget(self.time_max, 5, 0)
        
        self.btngroup1 = QButtonGroup()
        self.btngroup2 = QButtonGroup()
        
        # Podaj krok czasowy
        ukladH1 = QHBoxLayout()
        InfoDeltaTime = QLabel("Podaj krok czasowy.", self)
        ukladT.addWidget(InfoDeltaTime, 6, 0)
        
        self.delta_time = QRadioButton("0.05")
        self.delta_time.value=0.05
        self.btngroup1.addButton(self.delta_time)
        ukladH1.addWidget(self.delta_time)
        
        self.delta_time = QRadioButton("0.1")
        self.delta_time.value=0.1
        self.btngroup1.addButton(self.delta_time)
        ukladH1.addWidget(self.delta_time)
        
        
        self.delta_time = QRadioButton("0.2")
        self.delta_time.value=0.2
        self.btngroup1.addButton(self.delta_time)
        ukladH1.addWidget(self.delta_time)
        
        self.delta_time = QRadioButton("0.5")
        self.delta_time.value=0.5
        self.btngroup1.addButton(self.delta_time)
        
        ukladH1.addWidget(self.delta_time)
        
        ukladT.addLayout(ukladH1, 7, 0)
        
        
        # Wybór częstotliwości odświeżania
        ukladH3 = QHBoxLayout()
        InfoRefreshRate = QLabel("zaznacz częstotliwość z jaką chcesz odświeżać obraz.", self)
        ukladT.addWidget(InfoRefreshRate,8,0)
        
        self.refresh_rate = QRadioButton("30")
        self.refresh_rate.value=30
        self.btngroup2.addButton(self.refresh_rate)
        ukladH3.addWidget(self.refresh_rate)
        
        self.refresh_rate = QRadioButton("60")
        self.refresh_rate.value=60
        self.btngroup2.addButton(self.refresh_rate)
        ukladH3.addWidget(self.refresh_rate)
        
        
        self.refresh_rate = QRadioButton("120")
        self.refresh_rate.value=120
        self.btngroup2.addButton(self.refresh_rate)
        ukladH3.addWidget(self.refresh_rate)
        
        
        ukladT.addLayout(ukladH3, 9, 0)
        
        # Przycisk Ok
        ukladH4 = QHBoxLayout()
        self.OkBtn = QPushButton("&OK", self)
        self.OkBtn.clicked.connect(self.switch_result_window)
        ukladH4.addWidget(self.OkBtn)
        self.setLayout(ukladT)
        ukladT.addLayout(ukladH4, 10, 0)

        self.setGeometry(20, 20, 400, 100)
        self.setWindowTitle("NAZWA OKIENKA")
        self.center()
        self.show()
    
    def Calculations(self):
        number_of_time_periods = int((self.time_max.value()-time_min)//self.delta_time.value + 1)

        Coords = np.ndarray(shape=(self.particles_number.value(), number_of_time_periods, 3))

        Velocities = np.ndarray(shape=(self.particles_number.value(), 3))

        for i in range(self.particles_number.value()):
            Velocities[i,0]=np.random.uniform(low=-20,high=20)
            Velocities[i,1]=np.random.uniform(low=-20,high=20)
            Velocities[i,2]=np.random.uniform(low=-2,high=2)

        for i in range(self.particles_number.value()):
            #i-ta cząstka na polu (i,i,0)
            Coords[i,0,0]=np.random.uniform(low=-200,high=200)
            Coords[i,0,1]=np.random.uniform(low=-200,high=200)
            Coords[i,0,2]=np.random.uniform(low=-200,high=200)

        for i in range(self.particles_number.value()):
            for j in range(1,number_of_time_periods):
                for k in range(3):
                    Coords[i,j,k]=Coords[i,j-1,k]+Velocities[i,k]*self.delta_time.value
        return self.particles_number.value(), self.refresh_rate.value, self.Object.currentItem().text(), Coords
        
    
    @pyqtSlot()
    def switch_result_window(self):
        self.cams = ResultWindow(self.Calculations()) 
        self.btngroup2.addButton(self.refresh_rate)
    

class AuthorsWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()

    def center(self):
        frameGm = self.frameGeometry()
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
    
    def interfejs(self):
        Info1 = QLabel("Autorzy:", self)
        Info2 = QLabel(" 1) Paweł Lefelbajn", self)
        Info3 = QLabel(" 2) Michał Dybowski", self)
        Info4 = QLabel(" 3) Kacper Kurowski", self)
        ukladT = QGridLayout()
        ukladT.addWidget(Info1, 0, 0)
        ukladT.addWidget(Info2, 1, 0)
        ukladT.addWidget(Info3, 2, 0)
        ukladT.addWidget(Info4, 3, 0)
       
        self.returnBtn = QPushButton("&Powrót", self)
        self.returnBtn.clicked.connect(self.switch_start_window)
        ukladH1 = QHBoxLayout()
        ukladH1.addWidget(self.returnBtn)
        # przypisanie utworzonego układu do okna
        self.setLayout(ukladT)
        ukladT.addLayout(ukladH1, 4, 0)
        
        self.setGeometry(20, 20, 400, 300)
        self.setWindowTitle("Autorzy")
        self.center()
        self.show()
    

    @pyqtSlot()
    def switch_start_window(self):
        self.cams = StartWindow() 
        self.cams.show()
        self.close()
    
############################
############################
############################
############################

class ResultWindow(QWidget):

    def __init__(self, args ,parent=None):
        super().__init__(parent)

        self.interfejs(args)

    def center(self):
        frameGm = self.frameGeometry()
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
    
    def interfejs(self,args):
        self.particles_number = args[0]
        self.refresh_rate = args[1]
        self.Object = args[2]
        Coords = args[3]
        
        
        #Info1 = QLabel("Autorzy:", self)
        #Info2 = QLabel(f"{self.particles_number}", self)
        #Info3 = QLabel(f"{self.refresh_rate}", self)
        #Info4 = QLabel(f"{self.Object}", self)
        #ukladT = QGridLayout()
        #ukladT.addWidget(Info1, 0, 0)
        #ukladT.addWidget(Info2, 1, 0)
        #ukladT.addWidget(Info3, 2, 0)
        #ukladT.addWidget(Info4, 3, 0)
        
        #self.setLayout(ukladT)
        ### animacja
        #self.frame = Qt.QFrame()
        #elf.window = Qt.QMainWindow()
        #self.vl = Qt.QVBoxLayout()
        self.renderer = vtk.vtkRenderer()
        self.interactor = QVTKRenderWindowInteractor(self)
        self.window = self.interactor.GetRenderWindow()

        #self.vl.addWidget(self.vtkWidget)
        #self.frame.setLayout(self.vl)
        #self.renderer = vtk.vtkRenderer()
        #self.window = self.vtkWidget.GetRenderWindow()
        #self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()
        #
        # 
        self.interactor = prepare_animation(
                            self.renderer, 
                            self.window, 
                            self.interactor, 
                            Coords, 
                            self.particles_number,
                            self.refresh_rate,
                            stl_files[self.Object]
                            )
        self.interactor.Start()
        ###
        

        #self.ReturnBtn = QPushButton("&Powrót", self)
        #self.ReturnBtn.clicked.connect(self.switch_start_window)

        #self.vl.addWidget(self.ReturnBtn)


        self.setGeometry(20, 20, 400, 600)
        self.setWindowTitle("Wizualizacja")
        self.center()
        self.show()
    

    @pyqtSlot()
    def switch_start_window(self):
        self.cams = StartWindow() 
        self.cams.show()
        self.close()
    
###############################
###############################
###############################
###############################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = StartWindow()
    sys.exit(app.exec_())

