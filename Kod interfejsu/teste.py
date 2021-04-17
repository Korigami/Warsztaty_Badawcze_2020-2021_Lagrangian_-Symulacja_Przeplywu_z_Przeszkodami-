import sys
import vtk
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import Qt
import numpy as np

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class mainWindow(Qt.QMainWindow):
    def __init__(self, parent = None):
        Qt.QMainWindow.__init__(self, parent)

        self.frame = Qt.QFrame()
        self.vl = Qt.QVBoxLayout()
        self.button = QtWidgets.QPushButton("TestButton")
        self.label = QtWidgets.QLabel("This is a label")
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)

        #Create Source
        self.source = vtk.vtkCylinderSource()
        self.source.SetCenter(0, 0, 0)
        self.source.SetRadius(5.0)
        #Create Mapper
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.source.GetOutputPort())
        #Create Actor
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)

        #Create poke matrix for cylinder
        self.pMatrix = vtk.vtkMatrix4x4()

        self.vl.addWidget(self.vtkWidget)
        self.vl.addWidget(self.button)
        self.vl.addWidget(self.label)

        self.ren = vtk.vtkRenderer()
        self.ren.AddActor(self.actor)
        self.renWin = self.vtkWidget.GetRenderWindow()
        self.renWin.AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        #Settings
        self.ren.SetBackground(0.2, 0.2, 0.2)
        self.timeStep = 20 #ms
        self.total_t = 0

        #Inititalize Window, Interactor, Renderer, Layout
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()

        # Create Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerCallback)
        self.timer.start(self.timeStep)

    def timerCallback(self, *args):
        self.total_t += self.timeStep / 1000
        #Rotate Cylinder
        angle = 2 * np.pi * self.total_t
        rotMatrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                              [np.sin(angle), np.cos(angle), 0],
                                  [0, 0, 1]])
        for i in range(3):
            for j in range(3):
                self.pMatrix.SetElement(i, j, rotMatrix[i, j])

        self.actor.PokeMatrix(self.pMatrix)
        self.iren.Render() #NOT: self.ren.Render()


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())