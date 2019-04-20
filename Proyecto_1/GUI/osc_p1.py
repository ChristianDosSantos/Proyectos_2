import sys
import numpy as np
import matplotlib.pyplot  as plt
import matplotlib.animation as animation
from definitions3 import *


#Welcome
print('Bienvenido. Por favor siga las instrucciones para inicializar el software.\n')

#Choose OS and port
os = input('Indique su Sistema Operativo, Linux (1) or Windows (0): ')
if(os=='1'):
    Port='/dev/ttyUSB'  #ls -l  /dev/ttyUSB*
else:
    Port='COM'
Port = Port + input('Indique el número de puerto a usar: ')

#Graphing info
ts=250 #sampling time in ms
refresh_time=250 #time for updating graph in ms
scale_factor=5.0/4095
n_scaleX=10.0
n_scaleY=5.0
n_points=2000
n_block=500

#Communication object
try:
    con = flow_data(Port,n_points,scale_factor,n_block)
except:
    print('El número de puerto introducido no es válido, abortando ejecución...')
    exit()


#Run GUI
app = QtGui.QApplication(sys.argv)
window = MyApp(con,ts,refresh_time,n_scaleX,n_scaleY)
window.show()
sys.exit(app.exec_())

