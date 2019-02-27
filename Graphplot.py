import matplotlib
matplotlib.use('Qt4Agg')
import sys
from PyQt4 import QtCore, QtGui, uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

qtCreatorFile = "graph.ui" # my Qt Designer file 

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.navigation = NavigationToolbar(self.canvas,self)
        self.hlayout.addWidget(self.navigation)

        self.gCheck.stateChanged.connect(self.Grid)
        self.gCheck.setStatusTip("Colocar Grid en la gráfica")
        self.tBox.activated[str].connect(self.changeTimeScale)
        self.tBox.setStatusTip("Cambiar la escala temporal")
        self.aBox.activated[str].connect(self.changeAmpScale)
        self.aBox.setStatusTip("Cambiar la escala de Amplitud")

        self.plot()

    def Grid (self,state):
        if state == QtCore.Qt.Checked:
            print("Checked") #Colocar Grid
        else:
            print("Unchecked") #Quitar Grid
    
    def changeTimeScale(self,text):
        if text == "t = 1s":
            print("t = 1s") #Colocar cambio de escala
        elif text == "t = 100ms":
            print("t = 100ms") #Colocar cambio de escala
        else:
            print("t = 10ms") #Colocar cambio de escala
        
    def changeAmpScale(self,text):
        if text == "A = 1V":
            print("A = 1V") #Colocar cambio de escala
        elif text == "A = 100mV":
            print("A = 100mV") #Colocar cambio de escala
        else:
            print("A = 10mV") #Colocar cambio de escala
    
    def plot(self):
         #Colocar la funcion que comienza el plot
        x = [1,2,3,4,5]
        y = [2,4,6,8,10]
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(x,y)
        self.canvas.draw()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())        