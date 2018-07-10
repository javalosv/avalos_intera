from __future__ import division
import numpy as np
from math import *

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy

# Algoritm 
# http://www.personal.psu.edu/jjb23/web/htmls/sl455SP12/ch3/CH03_5C.pdf

x=np.linspace(0, 3, 7)
a=[-0.0497081518 ,   -0.0537617656 ,  -0.245754079 ,   -0.1561610521,   -0.4432674925 ,  -0.5804805548,   -0.9952186238]
f=100

FPO=0.0
FPN=0.0

n=len(a)-1;
l=np.arange(n+1, dtype=np.float_)
u=np.arange(n, dtype=np.float_)
z=np.arange(n+1, dtype=np.float_)
h=np.arange(n, dtype=np.float_)
alfa=np.arange(n+1, dtype=np.float_)
c=np.arange(n+1, dtype=np.float_)
b=np.arange(n, dtype=np.float_)
d=np.arange(n, dtype=np.float_)

for i in range(n):
    h[i]=x[i+1]-x[i]

sA = np.zeros(shape=(n+1,n+1), dtype=np.float_)
for i in range(0,n) :
    for j in range(0,n) :
        if i is j:
            sA[i+1][j+1]=2*(h[i-1]+h[i])
            sA[i+1][i]=h[0]
            sA[i][i+1]=h[0]
sA[0][0]=2*h[0]
sA[-1][-1]=2*h[-1]
            
sb = np.zeros(shape=(n+1,1), dtype=np.float_)

for i in range(1,n) :
	sb[i]=(3.0*(a[i+1]-a[i])/h[i]) - (3.0*(a[i]-a[i-1])/h[i-1])

sb[0]=((3.0*(a[1]-a[0]))/h[0])-3.0*FPO
sb[-1]=3.0*FPN-(3.0*(a[n]-a[n-1])/h[n-1])

_b=np.arange(n, dtype=np.float_)
_c=np.linalg.solve(sA, sb)
_d=np.arange(n, dtype=np.float_)

for j in reversed(range(n)):
    _b[j]=((a[j+1]-a[j])/h[j] )-(h[j]*(_c[j+1]+2*_c[j])/3.0)
    _d[j]=(_c[j+1]-_c[j])/(3.0*h[j])

# Graphic
t_out=np.linspace(x[0], x[-1], n*f+1)
s =[]

for j in range(n):
    _t=t_out[f*j:f*(j+1)]
    for i in range(len(_t)):
		s.append( float(a[j]+_b[j]*(_t[i]-x[j])+_c[j]*(_t[i]-x[j])**2+_d[j]*(_t[i]-x[j])**3))
s.append(float(a[-1]+_b[-1]*(t_out[-1]-x[-1])+_c[-1]*(t_out[-1]-x[-1])**2+_d[-1]*(t_out[-1]-x[-1])**3))
print("Puntos t:",len(t_out))
print("Puntos s:\n",s)
print 
plt.subplot(3, 1, 1)
plt.plot(x, a, 'bo')
plt.plot(t_out,s,'r-')

v0=[]
plt.subplot(3, 1, 2)
for n in range(len(s)-1):
    v0.append((s[n+1]-s[n])*f)
v0.append(v0[-1]) 
plt.plot(t_out,v0,'b-')

a0=[]
plt.subplot(3, 1, 3)
for n in range(len(v0)-1):
    a0.append((v0[n+1]-v0[n])*f)
a0.append(a0[-1]) 
plt.plot(t_out,a0,'r-')


plt.show()