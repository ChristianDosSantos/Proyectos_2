import sys
import serial
import numpy as np
import matplotlib.pyplot  as plt
import matplotlib.animation as animation
import time
import matplotlib
from PyQt4 import QtCore, QtGui, uic
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

#-------------------------------------------------------------------------
#Class implementations

class flow_data(serial.Serial):

    def __init__(self,Port,len_fifo,scale_factor,n_block):
        serial.Serial.__init__(self,
                               port=Port,
                               baudrate=115200,
                               parity=serial.PARITY_NONE,
                               stopbits=serial.STOPBITS_ONE,
                               bytesize=serial.EIGHTBITS,
                               timeout=1
                                )
        #Port init
        self.close()
        self.open()
        self.data_read=[0] * 4
        self.len_fifo=len_fifo
        self.data_fifo=np.zeros([len_fifo,4], dtype=np.float)
        self.scale_factor=scale_factor
        self.n=n_block

    def get(self): #Reads four byte convetions & stores it in self.data_read
        while True:
            r=ord(self.read(1))
            if r < 128:
                break
        self.data_read=[r]
        r=  self.read(3)
        for i in r:
            self.data_read.append(i)

    def get_block(self): #Reads four byte convetions & stores it in self.data_read
        while True:
            r=ord(self.read(1))
            if r < 128:
                break
        self.data_read=[r]
        r=self.read(4*self.n-1)
        for i in r:
            self.data_read.append(i)

    def decode(self,data): #Returns array with four decoded channels from data in self.data_read
        #Check for error
        is_err= (data[0] & 0xC0) != 0 or (data[1] & 0x80) == 0 or (data[2] & 0x80) == 0 or (data[3] & 0x80) == 0
        if(is_err):
            return 0, 0, 100, 100 #identify error
        else:
            #analog channels
            analogCh1= ((0x3F & data[0]) << 6) | (data[1] & 0x3F)
            analogCh2= ((0x3F & data[2]) << 6) | (data[3] & 0x3F)

            #digital channels
            digitalCh1, digitalCh2 = 0, 0
            if (data[2] & 0x40) != 0:
                digitalCh1=1
            if (data[3] & 0x40) != 0:
                digitalCh2=1

            return [analogCh1*self.scale_factor, analogCh2*self.scale_factor, digitalCh1, digitalCh2]

    def update_all(self): #Updata self.data_read, decode such data and stores it in self.data_fifo
        self.get()
        self.data_fifo=np.vstack((self.decode(self.data_read),self.data_fifo[:-1]))

    def update_all_block(self):
        self.get_block()        
        for i in range(self.n):
            r=self.decode(self.data_read[4*i:4*i+4])
            self.data_fifo=np.vstack((r,self.data_fifo[:-1]))
        #print(self.in_waiting)  #for debugging purposes only
        
    def set_fifo_len(self,len_fifo):  #Change fifo size
        self.len_fifo=len_fifo
        self.data_fifo=np.zeros([len_fifo,4], dtype=np.float)

    
#GUI CLASS
qtCreatorFile = "graph.ui" # my Qt Designer file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self,con,ts,refresh_time,n_scaleX,n_scaleY):
        QtGui.QMainWindow.__init__(self) #Main Window class
        Ui_MainWindow.__init__(self)
        self.setupUi(self) #Sets the GUI design from the .UI file
        self.navigation = NavigationToolbar(self.canvas,self) #Creates the toolbar for the plot
        self.hlayout.addWidget(self.navigation)

        self.gCheck.stateChanged.connect(self.Grid) #If grid button is checked executes Grid function
        self.gCheck.setStatusTip("Colocar Grid en la grafica")
        self.tBox.activated[str].connect(self.changeTimeScale) #If time selection is changed executes changeTimeScale function
        self.tBox.setStatusTip("Cambiar la escala temporal")
        self.aBox.activated[str].connect(self.changeAmpScale) #If Ampitude selection is changed executes changeAmpScale function
        self.aBox.setStatusTip("Cambiar la escala de Amplitud")
        self.cha1Box.stateChanged.connect(self.check_Chd2)   #If Channel button is checked executes check_Chd2 function
        self.cha2Box.stateChanged.connect(self.check_Cha2)  #If Channel button is checked executes check_Cha2 function
        self.chd1Box.stateChanged.connect(self.check_Cha1) #If Channel button is checked executes check_Cha1 function
        self.chd2Box.stateChanged.connect(self.check_Chd1) #If Channel button is checked executes check_Chd1 function
        self.con=con
        self.Ch_state=[False] * 4
        self.Ch_index=[]
        self.Ch_colors=['b','g','y','r']

        #graph settings
        print('Plotting...')
        self.voltageMax=5.0
        self.n_scaleX=n_scaleX #number of time div
        self.n_scaleY=n_scaleY #number of voltage div
        self.set_grid=False
        plt.ion()
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_xticklabels([]) #deletes labels from X-axes
        self.ax.set_ylim(0, self.voltageMax)
        plt.xticks(np.arange(0,self.con.len_fifo,self.con.len_fifo/self.n_scaleX)) #Defines div for X-axes
        plt.yticks(np.arange(0,self.voltageMax,self.voltageMax/self.n_scaleY)) #Defines div for Y-axes
        self.lines = self.ax.plot()
        plt.title('Oscilloscope')
        plt.xlabel('Time')
        plt.ylabel('Voltage')

        #Timer 1
        timer1=QtCore.QTimer(self)
        timer1.timeout.connect(self.con.update_all_block)
        timer1.start(ts)

        #Timer 2
        timer2=QtCore.QTimer(self)
        timer2.timeout.connect(self.refresh_image)
        timer2.start(refresh_time)

        con.set_buffer_size(rx_size = 10000, tx_size = 0)

    def plot_init(self):

        self.ax = self.canvas.figure.clear()
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_xticklabels([]) #deletes labels from X-axes
        self.ax.set_ylim(0, self.voltageMax)
        plt.xticks(np.arange(0,self.con.len_fifo,self.con.len_fifo/(self.n_scaleX-1))) #Defines div for X-axes
        plt.yticks(np.arange(0,self.voltageMax,self.voltageMax/(self.n_scaleY-1))) #Defines div for Y-axes
        if self.set_grid:
            self.ax.grid()
        self.lines=[]
        self.Ch_index=[]

        for i in range(len(self.Ch_state)):
            if self.Ch_state[i]:
                self.lines += self.ax.plot(self.con.data_fifo[:,i],self.Ch_colors[i])
                self.Ch_index.append(i)

        plt.title('Oscilloscope')
        plt.xlabel('Time')
        plt.ylabel('Voltage')



    def check_Cha1(self,state):  #If Channel button is checked shows the respective channel. Otherwise, it hides the channel
        if state == QtCore.Qt.Checked:
            self.Ch_state[0]=True
        else:
            self.Ch_state[0]=False
        self.plot_init()

    def check_Cha2(self,state): #If Channel button is checked shows the respective channel. Otherwise, it hides the channel
        if state == QtCore.Qt.Checked:
            self.Ch_state[1]=True
        else:
            self.Ch_state[1]=False
        self.plot_init()

    def check_Chd1(self,state): #If Channel button is checked shows the respective channel. Otherwise, it hides the channel
        if state == QtCore.Qt.Checked:
            self.Ch_state[2]=True
        else:
            self.Ch_state[2]=False
        self.plot_init()

    def check_Chd2(self,state): #If Channel button is checked shows the respective channel. Otherwise, it hides the channel
        if state == QtCore.Qt.Checked:
            self.Ch_state[3]=True
        else:
            self.Ch_state[3]=False
        self.plot_init()

    def refresh_image(self):
        for i in range(len(self.Ch_index)):
            self.lines[i].set_ydata(self.con.data_fifo[:,self.Ch_index[i]])
        self.canvas.draw()

    def Grid (self,state): #If Grid button is checked shows the Grid. Otherwise, it hides it
        if state == QtCore.Qt.Checked:
            self.set_grid=True
        else:
            self.set_grid=False
        self.plot_init()

    def changeTimeScale(self,text): #If box option is changed, changes the time scale
        if text == "t = 1s":
            self.con.set_fifo_len(2000) 
        elif text == "t = 100ms":
            self.con.set_fifo_len(200) 
        else:
            self.con.set_fifo_len(20) 

        self.plot_init()

    def changeAmpScale(self,text): #If box option is changed, changes the amplitude scale
        if text == "A = 1V":
            self.voltageMax=5
        elif text == "A = 100mV":
            self.voltageMax=0.5
        else:
            self.voltageMax=0.05
        self.plot_init()

#-------------------------------------------------------------------------
#Functions implementations

def get_data(con):
    while True:
        r=ord(con.read(1))
        if r < 128:
            break
    data=[r]
    r=con.read(3)
    for i in r:
        data.append(i)
    return data

def decode_data(packet):
    #Get bytes
    data=np.uint8(packet)
    #Check for error
    is_err= (data[0] & 0xC0) != 0 or (data[1] & 0x80) == 0 or (data[2] & 0x80) == 0 or (data[3] & 0x80) == 0
    if(is_err):
        return 0, 0, 100, 100 #identify error
    else:
        #analog channels
        analogCh1= ((0x3F & data[0]) << 6) | (data[1] & 0x3F)
        analogCh2= ((0x3F & data[2]) << 6) | (data[3] & 0x3F)

        #digital channels
        digitalCh1, digitalCh2 = 0, 0
        if (data[2] & 0x40) != 0:
            digitalCh1=1
        if (data[3] & 0x40) != 0:
            digitalCh2=1

        return analogCh1, analogCh2, digitalCh1, digitalCh2

def show_data(con):
    con.get()
    [analogCh1, analogCh2, digitalCh1, digitalCh2] = con.decode(con.data_read)
    print(100 * " ",end='\r')
    print('Analog Ch1: ',str(analogCh1),'  Analog Ch2: ',str(analogCh2),'  Digital Ch1: ',str(digitalCh1),'  Digital Ch2: ',str(digitalCh2), end='\r')
    sys.stdout.flush()





