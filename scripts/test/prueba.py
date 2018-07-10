
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev
from scipy import interpolate


import numpy as np
x=np.linspace(0, 6, 8)
a=[-0.0497081518,-0.0497081518 ,   -0.0537617656 ,  -0.245754079 ,   -0.1561610521,   -0.4432674925 ,  -0.5804805548,   -0.9952186238]
FPO=0
FPN=0

n=len(a);
h=[]
for i in range(n):
    h.append(x[n+1]-x[n])








#sp_0 = interpolate.CubicSpline(_time, y,bc_type=((1, 0.0), (1, 0.0)))
ts = np.linspace(_time[0], _time[-1], (_time[-1]-_time[0])*_f) 
q0= sp_0(ts)

#tck, u = splprep([ts, q0])
#new_points = splev(u, tck)

#fig, ax = plt.subplots()
#ax.plot(_time, y, 'ro')
#ax.plot(ts, q0, 'bo')
#ax.plot(new_points[0], new_points[1], 'r-')
#plt.show()



v0=[]
for n in range(len(q0)-1):
        v0.append((q0[n+1]-q0[n])*_f)
v0.append(v0[-1]) 




plt.subplot(2, 1, 1)
plt.plot(_time, y, 'bo')
plt.plot(ts,q0,'r-')

plt.subplot(2, 1, 2)
plt.plot(ts,v0,'r-')






plt.show()