import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import Qt, QtCore, QtGui, QtWidgets

import numpy as np
import time

import pyvista as pv

import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

import pickle
import sys, os

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir+"/PropagateParticles")

from propagate_particles import *

# STAŁE PARAMETRY
# ścieżka do plików z siatkami
path_to_stl = 'Siatki/'
stl_files = {
            'Krolik':path_to_stl+'Stanford_Bunny_sample.stl', 
            'Kostka Mengera' : path_to_stl+'Menger_sponge_sample.stl'
             }

NAZWA_APKI = "Symulacja przepływu z przeszkodami"
###################################
######  APLIKACJA OKIENKOWA  ######
###################################
class BaseWindow(QWidget):
    '''
        Podstawowe Okno z którego dziedziczą pozostałe
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 500, 100)
        self.setWindowTitle(f"{NAZWA_APKI}")
        self.center()

    def center(self):
        '''
            Funkcja wyświetlająca okno aplikacji w centrum aktywnie używanego ekranu
        '''
        frameGm = self.frameGeometry()
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

# Okno startowe
class StartWindow(BaseWindow):
    '''
        Okno startowe aplikacji
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.interfejs()
        self.show()

    def interfejs(self):
        ukladT = QGridLayout()
        
        Info = QLabel("Co chcesz zrobić?", self)
        ukladT.addWidget(Info, 0, 0)
        
        ukladH1 = QHBoxLayout()
        self.vizualizeBtn = QPushButton("&Wygeneruj", self)
        self.vizualizeBtn.clicked.connect(self.switch_vizualize_window)
        ukladH1.addWidget(self.vizualizeBtn)
        ukladT.addLayout(ukladH1, 1, 0, 1, 3)

        ukladH1 = QHBoxLayout()
        self.vizualizeBtn = QPushButton("&Wczytaj", self)
        self.vizualizeBtn.clicked.connect(self.switch_ChooseLoadObject_window)
        ukladH1.addWidget(self.vizualizeBtn)
        ukladT.addLayout(ukladH1, 2, 0, 1, 3)
        
        ukladH2 = QHBoxLayout()
        self.authorsBtn = QPushButton("&Autorzy", self)
        self.authorsBtn.clicked.connect(self.switch_authors_window)
        ukladH2.addWidget(self.authorsBtn)
        ukladT.addLayout(ukladH2, 3, 0, 1, 3)
    
        self.setLayout(ukladT)
       
    
    @pyqtSlot()
    def switch_vizualize_window(self):
        self.cams = VizualizeWindow() 
        self.cams.show()
        self.close()

    @pyqtSlot()
    def switch_ChooseLoadObject_window(self):
        self.cams = ChooseLoadObjectWindow() 
        self.cams.show()
        self.close()

    @pyqtSlot()
    def switch_authors_window(self):
        self.cams = AuthorsWindow() 
        self.cams.show()
        self.close()

# Autorzy
class AuthorsWindow(BaseWindow):
    '''
        Okno wyświetlające autorów
    '''
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

# Wczytywanie pickla
class ChooseLoadObjectWindow(BaseWindow):
    '''
        Okno do wczytywania gotowych plików .pkl do symulacji
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.interfejs()
        self.show()
    
    def Load(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self,"Wybierz pickla do wczytania","PickleSample","(*.pkl)", options=options)
        if filename:
            with open(filename, mode ='rb') as f:
                Coords = pickle.load(f)
            number_of_time_periods = Coords.shape[1]
            Object = self.Object.currentItem().text()
            save = False if self.save == "Nie" else self.save
            return number_of_time_periods, Object, Coords, save
    
    def choose_object(self,ukladT):
        InfoObject = QLabel("wybierz obiekt", self)
        ukladT.addWidget(InfoObject, 0, 0)
        
        self.Object = QListWidget(self)
        #self.Object.setGeometry(50, 70, 100, 60)
        item1 = QListWidgetItem("Krolik")
        item3 = QListWidgetItem("Kostka Mengera")
        self.Object.addItem(item1)
        self.Object.addItem(item3)
        ukladT.addWidget(self.Object, 1, 0)
        
        
    def btnstate(self,b):
        if b.isChecked() == True:
            self.save = b.text()
        
    def choose_if_save(self,ukladT):
        
        InfoObject = QLabel("Czy chcesz zapisać animację?", self)
        ukladT.addWidget(InfoObject, 8, 0)
        
        layout = QHBoxLayout()
        
        self.b1 = QRadioButton("Nie")
        self.b1.setChecked(True)
        self.save = "Nie"
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        layout.addWidget(self.b1)
        
        self.b2 = QRadioButton("avi")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))
        layout.addWidget(self.b2)
        
        ukladT.addLayout(layout, 9, 0)
    
    def interfejs(self):
        ukladT = QGridLayout()
        
        self.choose_object(ukladT)  # Wybór obiektu
        self.choose_if_save(ukladT)
        ##### Przycisk Ok
        ukladH = QHBoxLayout()
        self.OkBtn = QPushButton("&OK", self)
        self.OkBtn.clicked.connect(self.switch_result_window)
        ukladH.addWidget(self.OkBtn)
        ukladT.addLayout(ukladH, 10, 0)
        ########
        
        self.setLayout(ukladT)
            
    
    @pyqtSlot()
    def switch_result_window(self):
        self.cams = ResultWindow(self.Load())
        self.cams.show()
        self.close() 

# Generowanie Pickla
class VizualizeWindow(BaseWindow):
    '''
        Okno w którym ustawia sie parametry i wywołuje algorytm wyznaczania trajektori cząsteczek.
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.interfejs()
        self.show()

    def choose_object(self,ukladT):
        InfoObject = QLabel("wybierz obiekt", self)
        ukladT.addWidget(InfoObject, 0,0)
        
        self.Object = QListWidget(self)
        item1 = QListWidgetItem("Krolik")
        item3 = QListWidgetItem("Kostka Mengera")
        self.Object.addItem(item1)
        self.Object.addItem(item3)
        ukladT.addWidget(self.Object,1,0)
    
    def choose_direction(self,ukladT):
        InfoDirection = QLabel("wybierz scenariusz", self)
        ukladT.addWidget(InfoDirection, 0,1)
        
        self.Direction = QListWidget(self)
        item1 = QListWidgetItem("UP_DOWN")
        item2 = QListWidgetItem("DOWN_UP")
        item3 = QListWidgetItem("LEFT_RIGHT")
        item4 = QListWidgetItem("RIGHT_LEFT")
        item5 = QListWidgetItem("FRONT_BACK")
        item6 = QListWidgetItem("BACK_FRONT")
        self.Direction.addItem(item1)
        self.Direction.addItem(item2)
        self.Direction.addItem(item3)
        self.Direction.addItem(item4)
        self.Direction.addItem(item5)
        self.Direction.addItem(item6)
        ukladT.addWidget(self.Direction,1,1)    
    
    
    def set_QSpinBox(self,ukladT,message,max_value,min_value,deafult_value,i,j):
        Info= QLabel(message, self)
        ukladT.addWidget(Info, i,j)
        spinbox = QSpinBox()
        spinbox.setMinimum(min_value)
        spinbox.setMaximum(max_value)
        spinbox.setValue(deafult_value)
        ukladT.addWidget(spinbox, i+1, j)
        return spinbox
    
    def set_QDoubleSpinBox(self,ukladT,message,max_value,min_value,deafult_value,decimals,i,j):
        Info= QLabel(message, self)
        ukladT.addWidget(Info, i,j)
        doubleSpinbox = QDoubleSpinBox()
        doubleSpinbox.setMinimum(min_value)
        doubleSpinbox.setMaximum(max_value)
        doubleSpinbox.setValue(deafult_value)
        doubleSpinbox.setDecimals(decimals)
        ukladT.addWidget(doubleSpinbox, i+1, j)
        return doubleSpinbox
        
    
    def btnstate(self,b):
        if b.isChecked() == True:
            self.save = b.text()
        
    def choose_if_save(self,ukladT,i,j):
        
        InfoObject = QLabel("Czy chcesz zapisać animację?", self)
        ukladT.addWidget(InfoObject, i,j)
        
        layout = QHBoxLayout()
        
        self.b1 = QRadioButton("Nie")
        self.b1.setChecked(True)
        self.save = "Nie"
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        layout.addWidget(self.b1)
        
        self.b2 = QRadioButton("avi")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))
        layout.addWidget(self.b2)
        
        ukladT.addLayout(layout,i,j+1)
        
    def interfejs(self):
        ukladT = QGridLayout()
                
        self.choose_object(ukladT)  # Wybór obiektu
        self.choose_direction(ukladT)
        self.particles_number = self.set_QSpinBox(ukladT,"liczba cząsteczek",1000000,1,1000,2,0) # liczba cząsteczek
        self.number_of_time_periods = self.set_QSpinBox(ukladT,"liczba iteracji",10000,1,2000,4,0) # liczba kroków czasowych
        self.delta_time = self.set_QSpinBox(ukladT,"krok czasowy (w ms).",1000,1,10,6,0)# długośc kroków czasowych
        self.mass = self.set_QDoubleSpinBox(ukladT,"masa cząsteczek (kg)",1,0,0.1,3,8,0) # masa cząsteczki
        self.cross_area = self.set_QDoubleSpinBox(ukladT,"pole przekroju poprzecznego cząsteczek",1,0.001,0.01,3,10,0) # pole przekroju cząsteczki
        self.speed = self.set_QDoubleSpinBox(ukladT,"szybkość cząsteczek",20,0,7,3,12,0) # szybkość cząsteczek
        
        self.gravity = self.set_QDoubleSpinBox(ukladT,"przyspieszenie grawitacyjne",20,-20,9.81,3,2,1) # przyspieszenie grawitacyjne
        self.friction = self.set_QDoubleSpinBox(ukladT,"współczynnik tarcia z powietrzem",1,0.001,0.04,3,4,1) # współczynnik tarcia
        self.wind_x = self.set_QDoubleSpinBox(ukladT,"współrzędna x prędkości wiatru ",20,-20,5,2,6,1) # prędkośc wiatru x
        self.wind_y = self.set_QDoubleSpinBox(ukladT,"współrzędna y prędkości wiatru",20,-20,10,2,8,1) # prędkośc wiatru y
        self.wind_z = self.set_QDoubleSpinBox(ukladT,"współrzędna z prędkości wiatru",20,-20,10,2,10,1) # prędkośc wiatru z
        self.air_density = self.set_QDoubleSpinBox(ukladT,"gęstość powietrza",1,0.001,0.02,3,12,1) # gęstość powietrza
    
        
        
        self.choose_if_save(ukladT,14,0) # Czy zapisujemy
        ##### Przycisk Ok
        ukladH = QHBoxLayout()
        self.OkBtn = QPushButton("&OK", self)
        self.OkBtn.clicked.connect(self.switch_result_window)
        ukladH.addWidget(self.OkBtn)
        ukladT.addLayout(ukladH, 15, 0,15,2)
        ########
        
        self.setLayout(ukladT)
    
    
    def Calculations(self):
        '''
            Tutaj pojawia się wywołanie algorytmu na podanych przez użytkownika parametrach
        '''
        save = False if self.save == "Nie" else self.save
        particles_number = self.particles_number.value()
        number_of_time_periods = self.number_of_time_periods.value()
        Object = self.Object.currentItem().text()
        Direction = self.Direction.currentItem().text()
        delta_time = self.delta_time.value()
        mass = self.mass.value()
        gravity = self.gravity.value()
        wind_x = self.wind_x.value()
        wind_y = self.wind_y.value()
        wind_z = self.wind_z.value()
        friction = self.friction.value()
        cross_area = self.cross_area.value()
        air_density = self.air_density.value()
        speed = self.speed.value()
        #### Tutaj wyznaczanie coords
        Coords = propagate_particles(
            Object,
            delta_time/1000,
            number_of_time_periods,
            particles_number,
            None,
            None,
            np.array([mass]*particles_number),
            np.array([cross_area]*particles_number),
            Constants(
                np.array([0,0,-gravity]),
                friction,
                air_density,
                np.array([wind_x,wind_y,wind_z])
                ),
            speed,
            n_triangles = 0,
            direction = Direction)
        ####
        
        return number_of_time_periods, Object, Coords, save
        
    
    @pyqtSlot()
    def switch_result_window(self):
        self.cams = ResultWindow(self.Calculations())
        self.cams.show()
        self.close() 
    

class ResultWindow(BaseWindow):
    '''
        Okno odpowiadające za wywołanie animacji. 
        Istnieje możliwość zapisania wygenerowanej trajektori do pliku w rozszerzeniu .pkl
    '''
    def __init__(self, args, parent=None): 
        super().__init__(parent)       
        self.interfejs(args)
        self.show()

    def single_animation(self,j, Coords):
        points = Coords[:,j,:]
        point_cloud = pv.PolyData(points)
        self.plotter.add_mesh(
                    point_cloud,
                    name = f"a",
                    smooth_shading=True,
                    color = 'red'
                    )
                        
    def animate(self,number_of_time_periods, Coords, save, movie_name = None):
        if save == "avi":
            self.plotter.open_movie(f"{movie_name}.avi",framerate = 10)
        for j in range(number_of_time_periods):
            #start_time = time.time()
            self.single_animation(j, Coords)
            if save :
                self.plotter.write_frame()
            #print("--- %s seconds ---" % (time.time() - start_time))
        self.plotter.close()
    
    def save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self,"Zapis ruchu cząsteczek","PickleSample"," (*.pkl)", options=options)
        if filename:
            if filename[-3:] != "pkl":
                filename+=".pkl"
            with open(filename,'wb') as f: 
                pickle.dump(self.Coords, f)


    def interfejs(self,args):
        ukladT = QGridLayout()
        number_of_time_periods = args[0]
        Object = args[1]
        self.Coords = args[2]
        save = args[3]
        
        if not save:
            self.plotter = pv.Plotter(window_size=[1856,1024],line_smoothing =True, point_smoothing= True, polygon_smoothing = True)
        else:
            self.plotter = pv.Plotter(window_size=[1856,1024],line_smoothing =True, point_smoothing= True, polygon_smoothing = True)#,off_screen=True,)
        self.plotter.set_background(color='white')
        self.mesh = pv.PolyData(stl_files[Object])
        self.plotter.add_mesh(self.mesh ,name = f"{Object}", color = 'green')
        self.plotter.show(auto_close=False)
        
        if save:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            movie_name, _ = QFileDialog.getSaveFileName(self,"Zapisywanie filmu","MovieSample",f" (*.{save})", options=options)
            self.animate(number_of_time_periods,
                    self.Coords, 
                    save,
                    movie_name)
        else:
            self.animate(number_of_time_periods,
                    self.Coords, 
                    save)
        
        self.returnbtn = QPushButton("&Zamknij", self)
        self.returnbtn.clicked.connect(self.close_window)
        
        self.saveAndReturnbtn = QPushButton("&Zapisz trajektorię i zamknij", self)
        self.saveAndReturnbtn.clicked.connect(self.save_and_close_window)

        ukladH1 = QHBoxLayout()
        ukladH1.addWidget(self.returnbtn)
        ukladH1.addWidget(self.saveAndReturnbtn)

        ukladT.addLayout(ukladH1, 1, 0, 1, 3)
              
        self.setLayout(ukladT)
        
    @pyqtSlot()
    def close_window(self):
        self.plotter.close()
        self.close()
        
    @pyqtSlot()
    def save_and_close_window(self):
        self.save()
        self.plotter.close()
        self.close()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = StartWindow()
    sys.exit(app.exec_())

