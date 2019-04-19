import sys
import numpy as np
import matplotlib.pyplot  as plt
import matplotlib.animation as animation
from definitions3 import *


#Welcome
print('Hello! Thank you using our service. Follow the steps for easy usage:')

#Choose OS
os = input('Please choose your OS, Linux (1) or Windows (0): ')
if(os=='1'):
    Port='/dev/ttyUSB0'  #ls -l  /dev/ttyUSB*
else:
    Port='COM3'

#Graphing info
ts=250 #sampling time in ms
refresh_time=250 #time for updating graph in ms
scale_factor=5.0/4095
n_scaleX=10.0
n_scaleY=5.0
n_points=2000
n_block=500

#Communication object
con = flow_data(Port,n_points,scale_factor,n_block)

mode = input('Choose an option, see measures (1) or graph (0): ')
if(mode=='1'):
    #Welcome
    print("Measure from the ADC:\n")
    while True:
        show_data(con)
else:
    app = QtGui.QApplication(sys.argv)
    window = MyApp(con,ts,refresh_time,n_scaleX,n_scaleY)
    window.show()
    sys.exit(app.exec_())
