from __future__ import division
import numpy as np
from math import *

import matplotlib.pyplot as plt
#import plotly.plotly as py
#from plotly.tools import FigureFactory as FF
#import plotly.graph_objs as go

import numpy as np
import pandas as pd
import scipy



# http://www.personal.psu.edu/jjb23/web/htmls/sl455SP12/ch3/CH03_5C.pdf

x=np.linspace(0, 3, 4)
#a=[-0.0497081518 ,   -0.0537617656 ,  -0.245754079 ,   -0.1561610521,   -0.4432674925 ,  -0.5804805548,   -0.9952186238]
a=np.exp(x)
print "a",a,"\n"
FPO=1.0
FPN=exp(3.0)
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
print "h", h, "\n"


A = np.zeros(shape=(n+1,n+1), dtype=np.float_)
B = np.zeros(shape=(n+1,n+1), dtype=np.float_)


for i in range(0,n) :
    for j in range(0,n) :
        if i is j:
            A[i+1][j+1]=2*(h[i-1]+h[i])
            A[i+1][i]=h[0]
            A[i][i+1]=h[0]
A[0][0]=2*h[0]
A[-1][-1]=2*h[-1]
            
_b = np.zeros(shape=(n+1,1), dtype=np.float_)

for i in range(1,n) :
    print "i",i
    _b[i]=(3.0*(a[i+1]-a[i])/h[i]) - (3.0*(a[i]-a[i-1])/h[i-1])

_b[0]=((3.0*(a[1]-a[0]))/h[0])-3.0*FPO
_b[-1]=3.0*FPN-(3.0*(a[n]-a[n-1])/h[n-1])

print "_b",_b
_c = np.linalg.solve(A, _b)
print "c",_c

_d=np.arange(n, dtype=np.float_)
for j in reversed(range(n)):
    print j
    #c[j]=z[j]-u[j]*c[j+1]
    #b[j]=((a[j+1]-a[j])/h[j] )-(h[j]*(c[j+1]+2*c[j])/3.0)
    _d[j]=(_c[j+1]-_c[j])/(3.0*h[j])

print "_d",_d




#STEP 2

alfa[0]=((3.0*(a[1]-a[0]))+h[0])-3.0*FPO#primer alfa
#alfa[0]=a[1]-a[0]#primer alfa

print "alfa 0", alfa[0]
alfa[n]=3.0*FPN-(3.0*(a[n]-a[n-1])/h[n-1])
#STEP 3
for i in range(1,n):
    alfa[i]=(3.0*(a[i+1]-a[i])/h[i]) - (3.0*(a[i]-a[i-1])/h[i-1])
    
print "alfa", alfa , "\n"

#STEP 4
l[0]=2.0*h[0]
u[0]=0.5
z[0]=alfa[0]/l[0]
#STEP 5
for i in range(1,n):
    l[i]=2.0*(x[i+1]-x[i-1])-h[i-1]*u[i-1]
    u[i]=h[i]/l[i]
    z[i]=(alfa[1]-h[i-1]*z[i-1])/l[i]

#STEP 6
l[n]=(h[n-1]*(2.0-u[n-1]))
z[n]=(alfa[n]-h[n-1]*z[n-1])/l[n]

#STEP 7 
c[n]=z[n]
for j in reversed(range(n)):
    print j
    c[j]=z[j]-u[j]*c[j+1]
    b[j]=((a[j+1]-a[j])/h[j] )-(h[j]*(c[j+1]+2*c[j])/3.0)
    d[j]=(c[j+1]-c[j])/(3.0*h[j])



print "a:",a,"\n"
print "b:",b,"\n"
print "c:",c,"\n"
print "d:",d,"\n"

# # Graphic
# f=10
# t_out=np.linspace(x[0], x[-1], n*f+1)
# s=[]
# print "periodo", f
# for j in range(n):
#     print "j",j
#     _t=t_out[f*j:f*(j+1)]
#     for i in range(len(_t)):
#         #print "i",i
#         #print "valor",_t[i]-x[j]
#         s.append( a[j]+b[j]*(_t[i]-x[j])+c[j]*(_t[i]-x[j])**2+d[j]*(_t[i]-x[j])**3)
# s.append(a[-1]+b[-1]*(t_out[-1]-x[-1])+c[-1]*(t_out[-1]-x[-1])**2+d[-1]*(t_out[-1]-x[-1])**3)

# print("s",len(s))
# print(len(t_out))

# plt.subplot(2, 1, 1)
# plt.plot(x, a, 'bo')
# plt.plot(t_out,s,'r*')



# v0=[]
# plt.subplot(2, 1, 2)
# for n in range(len(s)-1):
#         v0.append((s[n+1]-s[n])*f)
# v0.append(v0[-1]) 
# plt.plot(t_out,v0,'r*')

# plt.show()