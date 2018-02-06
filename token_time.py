import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure()

#x_values = [500000,1000000,10000000,20000000,30000000]
#y_values_80 = [6.21,14.84,136.95,266.59,375.52]     
#y_values_112 = [8.25,15.06,154.12,286.51,432.87]     
#y_values_128 = [8.64,16.04,163.40,335.43,494.59]     
#y_values_192 = [11.09,23.96,233.69,517.51,737.82]     
#xticks=['500t','1m','10m','20m','30m']
x_values = [2**6,2**7,2**8,2**9,2**10,2**12]
y_values_ST = [7,10,26,39,57,78]     
y_values_S3 = [4,6,10,20,28,45]     
xticks=['2^6','2^7','2^8','2^9','2^10','2^12']
ax = plt.gca()
ax.set_xscale('log')

plt.plot(x_values, y_values_ST,'-gv')
plt.plot(x_values, y_values_S3,'-r+')
plt.legend(['ST','S^3'], loc='upper left')
plt.xticks(x_values,xticks)

fig.suptitle('Query Computation time')
plt.xlabel('#Characters in the query')
plt.ylabel('Time in ms')
plt.autoscale(enable=True, axis='x', tight=True)#plt.axis('tight')

plt.grid()
fig.savefig('token_time_plot.pdf')
plt.show()
