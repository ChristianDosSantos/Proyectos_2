import matplotlib
matplotlib.use('Qt4Agg')
import sys
from PyQt4 import QtCore, QtGui, uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import warnings
warnings.filterwarnings('error')

qtCreatorFile = "Sensor_2.ui" # my Qt Designer file 

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

a = 1
b = 2

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #self.textBrowser_2.setText("Y Axis=0.0")
        #self.textBrowser_2.setFont(QtGui.QFont("Ubuntu Italic",18))
        #self.textBrowser_2.setAlignment(QtGui.AlignCenter)
        self.plot()
        self.toolbar_1 = NavigationToolbar(self.graph_1,self)
        self.verticalLayout_1.addWidget(self.toolbar_1)
        self.toolbar_2 = NavigationToolbar(self.graph_2,self)
        self.verticalLayout_2.addWidget(self.toolbar_2)
        timer = QtCore.QTimer(self)
        #timer.timeout.connect(self.tick(int(a), int(b))
        timer.timeout.connect(lambda: self.tick(int(a),int(b)))
        timer.timeout.connect(lambda: self.act())
        timer.start(1000)
        #self.tick()
        self.progressBar_1.setValue(100)
        self.progressBar_2.setValue(0)
 
    def tick (self,a,b):
        self.textBrowser_i.setText("X Axis =" )
        self.textBrowser_i.append(str(a))
        self.textBrowser_i.setFont(QtGui.QFont("Ubuntu Medium Bold",18))
        self.textBrowser_2.setText("Y Axis =")
        self.textBrowser_2.append(str(b))
        self.textBrowser_2.setFont(QtGui.QFont("Ubuntu Italic",18))
    
    def act (self):
        global a
        global b
        a = a + 1
        b = b + 1
        if a == 10:
            a = 1
        if b == 10:
            b = 1

    def plot(self):
        #Colocar la funcion que comienza el plot
        x = [1,2,3,4,5]
        y = [2,4,6,8,10]
        ax = self.graph_1.figure.add_subplot(111)
        ax.plot(x,y)
        self.graph_1.draw()
        ax = self.graph_2.figure.add_subplot(111)
        y = [1,4,9,16,25]
        ax.plot(x,y)
        self.graph_2.draw()

       

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_()) 