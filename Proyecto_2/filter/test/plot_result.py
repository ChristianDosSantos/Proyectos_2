import sys
import numpy as np
import matplotlib.pyplot  as plt

#File handing
file = open('test/filter.dat','r')
data=file.read()
data=data.split(',')  
data=np.array(data, dtype=int) #array of filter results

#Plotting
n_scale=10
y_max=2000
plt.plot(np.sin(data))
plt.title('Filter unitary step response')
plt.xlabel('Discrete time [n]')
plt.ylabel('Filter output')
plt.xticks(np.arange(0,len(data),len(data)/n_scale))
plt.yticks(np.arange(0,y_max,y_max/n_scale))  
plt.show()
