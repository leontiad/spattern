import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure()

#x_values = [500000,1000000,10000000,20000000,30000000]
#y_values_80 = [6.21,14.84,136.95,266.59,375.52]     
#y_values_112 = [8.25,15.06,154.12,286.51,432.87]     
#y_values_128 = [8.64,16.04,163.40,335.43,494.59]     
#y_values_192 = [11.09,23.96,233.69,517.51,737.82]     
#xticks=['500t','1m','10m','20m','30m']
x_values = [64,128,256,512]
y_values_1m = [60,69,87,100]     
y_values_100k = [4.23,5.65,7.74,7.84]     
y_values_10k = [1.46,1.47,1.49,1.58]     
xticks=['64','128','256','512']
ax = plt.gca()
ax.set_xscale('log')

plt.plot(x_values, y_values_1m,'-gv')
plt.plot(x_values, y_values_100k,'-r+')
plt.plot(x_values, y_values_10k,'-b*')
plt.legend(['|10^6| dataset ','|10^5| dataset','|10^4| dataset'], loc='upper left')
plt.xticks(x_values,xticks)

#fig.suptitle('Response Computation time for ST scheme [9]')
plt.xlabel('Query size in characters')
plt.ylabel('Time seconds')
plt.autoscale(enable=True, axis='x', tight=True)#plt.axis('tight')

plt.grid()
fig.savefig('response_plot_ST.pdf')
plt.show()
