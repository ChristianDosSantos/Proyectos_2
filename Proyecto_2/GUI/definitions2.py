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
import warnings
warnings.filterwarnings('error')

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

        #more
        self.data_fifo_prev=np.zeros([len_fifo,4], dtype=np.float)
        self.data_fifo_dif=np.zeros([len_fifo,4], dtype=np.float)

        #events
        self.is_event_fall_x=False
        self.is_event_fall_y=False
        self.event_fall_th=15 
        self.is_event_dif=False
        self.event_dif_th=5 
        self.x_mean=0
        self.y_mean=0       
        
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

    #Angles function: return orientation in degrees based on accelerometer measures
    def angles(self,vx,vy):  #g_vector must be a numpy array of the form [gx gy]
        m=6.62
        b=-7.94
        gx=(m*vx)+b
        gy=(m*vy)+b
        try:     
            alfa=np.arcsin(gy/9.8)
            beta=np.arcsin(gx/np.sqrt(96.04-np.power(gy,2)))
        except:
            alfa=np.pi/2
            beta=np.pi/2

        return alfa*(180/np.pi), beta*(180/np.pi)

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

            
            analogCh1, analogCh2 = self.angles(self.scale_factor*analogCh1, self.scale_factor*analogCh2 )

            return [analogCh1, analogCh2, digitalCh1, digitalCh2]

    def update_all(self): #Updata self.data_read, decode such data and stores it in self.data_fifo
        self.get()
        self.data_fifo=np.vstack((self.decode(self.data_read),self.data_fifo[:-1]))

    def update_all_block(self):
        self.get_block()   
        self.data_fifo_prev=self.data_fifo 
        for i in range(self.n):
            r=self.decode(self.data_read[4*i:4*i+4])
            self.data_fifo=np.vstack((r,self.data_fifo[:-1]))
        self.x_mean=np.mean(self.data_fifo[:,0])
        self.y_mean=np.mean(self.data_fifo[:,1])
        self.is_event_fall_x=np.abs(self.x_mean) > self.event_fall_th
        self.is_event_fall_y=np.abs(self.y_mean) > self.event_fall_th
        self.is_event_dif =np.mean(abs(self.data_fifo[:,0:1]-self.data_fifo_prev[:,0:1])) > self.event_dif_th


        #print(self.in_waiting)  #for debugging purposes only
        
    def set_fifo_len(self,len_fifo):  #Change fifo size
        self.len_fifo=len_fifo
        self.data_fifo=np.zeros([len_fifo,4], dtype=np.float)


    
#-------------------------------------------------------------------------
#GUI CLASS
qtCreatorFile = "Sensor_4.ui" # my Qt Designer file
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
        self.con=con
        self.Ch_state=[True, True, False, False]
        self.Ch_index=[]
        self.Ch_colors=['b','g','y','r']

        #graph settings
        print('Plotting...')
        self.voltageMax=3.0
        self.n_scaleX=n_scaleX #number of time div
        self.n_scaleY=n_scaleY #number of voltage div
        self.set_grid=False
        plt.ion()
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_xticklabels([]) #deletes labels from X-axes
        self.ax.set_ylim(0, self.voltageMax)
        plt.xticks(np.arange(-100,110,1)) #Defines div for X-axes
        plt.yticks(np.arange(-100,110,1)) #Defines div for Y-axes
        self.lines = self.ax.plot()
        
        #Timer 1
        timer1=QtCore.QTimer(self)
        timer1.timeout.connect(self.con.update_all_block)
        timer1.start(ts)

        #Timer 2
        timer2=QtCore.QTimer(self)
        timer2.timeout.connect(self.refresh_image)
        timer2.start(refresh_time)

        con.set_buffer_size(rx_size = 15000, tx_size = 0)
        self.plot_init();

    def plot_init(self):

        self.ax = self.canvas.figure.clear()
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_xticklabels([]) #deletes labels from X-axes
        self.ax.set_ylim(0, self.voltageMax)
        plt.xticks(np.arange(0,self.con.len_fifo,self.con.len_fifo/(self.n_scaleX-1)))
        plt.yticks(np.arange(-100,110,10)) #Defines div for Y-axes
        if self.set_grid:
            self.ax.grid()
        self.lines=[]
        self.Ch_index=[]

        for i in range(len(self.Ch_state)):
            if self.Ch_state[i]:
                self.lines += self.ax.plot(self.con.data_fifo[:,i],self.Ch_colors[i])
                self.Ch_index.append(i)

        plt.title('Orientaciones')
        plt.xlabel('Tiempo')
        plt.ylabel('Inclinación')
    
   
    def refresh_image(self):
        for i in range(len(self.Ch_index)):
            self.lines[i].set_ydata(self.con.data_fifo[:,self.Ch_index[i]])
            #events

            if self.con.is_event_fall_x:
                self.progressBar_x.setValue(100)
                self.textBrowser_xd.setText('PELIGRO: Caída en eje X')
                self.textBrowser_xd.setFont(QtGui.QFont("Ubuntu Medium Bold",10))
            else:
                self.progressBar_x.setValue(0)
                self.textBrowser_xd.setText('Estable')
                self.textBrowser_xd.setFont(QtGui.QFont("Ubuntu Medium Bold",14))
            if self.con.is_event_fall_y:
                self.progressBar_y.setValue(100)
                self.textBrowser_yd.setText('PELIGRO: Caída en eje Y')
                self.textBrowser_yd.setFont(QtGui.QFont("Ubuntu Medium Bold",10))
            else:
                self.progressBar_y.setValue(0)
                self.textBrowser_yd.setText('Estable')
                self.textBrowser_yd.setFont(QtGui.QFont("Ubuntu Medium Bold",14))

            if self.con.is_event_dif:
                self.progressBar_des.setValue(100)
                self.textBrowser_des.setText('PELIGRO: Movimiento')                
                self.textBrowser_des.setFont(QtGui.QFont("Ubuntu Medium Bold",10))
            else:                
                self.progressBar_des.setValue(0)
                self.textBrowser_des.setText('Estable')
                self.textBrowser_des.setFont(QtGui.QFont("Ubuntu Medium Bold",14))


            #Show angle values
            self.textBrowser_x.setText("X Axis =" + str(np.array(self.con.x_mean,dtype='int')) )       
            self.textBrowser_x.setFont(QtGui.QFont("Ubuntu Medium Bold",18))
            self.textBrowser_y.setText("Y Axis =" + str(np.array(self.con.y_mean,dtype='int')) )       
            self.textBrowser_y.setFont(QtGui.QFont("Ubuntu Medium Bold",18))

            self.canvas.draw()

            

    def Grid (self,state): #If Grid button is checked shows the Grid. Otherwise, it hides it
        if state == QtCore.Qt.Checked:
            self.set_grid=True                  
        else:
            self.set_grid=False            
        self.plot_init()





