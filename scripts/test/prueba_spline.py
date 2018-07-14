import numpy as np
import matplotlib.pyplot as plt

f=20
x=[0.0, 2.7489635262192884, 3.588031681391703, 4.4050473465254107, 5.1140515212826916, 5.9773635998267531, 8.5692968627530455] 

a= [-2.94436678, 2.41022146,  2.00620887,  1.49225344, 2.12876905, 2.51520289,-2.53351283] 


#x=np.linspace(0, 3, 4)
#a=np.exp(x)

FPO=0.0
FPN=0.0

n=len(a)-1;
l=np.zeros(n+1, dtype=np.float_)
u=np.zeros(n, dtype=np.float_)
z=np.zeros(n+1, dtype=np.float_)
h=np.zeros(n, dtype=np.float_)
alfa=np.zeros(n+1, dtype=np.float_)
c=np.zeros(n+1, dtype=np.float_)
b=np.zeros(n, dtype=np.float_)
d=np.zeros(n, dtype=np.float_)

for i in range(n):
	h[i]=x[i+1]-x[i]
print "h", h
sA = np.zeros(shape=(n+1,n+1), dtype=np.float_)
for i in range(n-1) :
	for j in range(n-1) :
		if i is j:
			print i
			sA[i+1][i+1]=2*(h[i]+h[i+1])
			sA[i+1][i]=h[i]
			sA[i][i+1]=h[i]
sA[0][0]=2*h[0]
sA[-1][-1]=2*h[-1]
sA[-1][-2]=h[-1]
sA[-2][-1]=h[-1]

			
print sA
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
t_out=np.linspace(x[0], x[-1], int((x[-1]-x[0])*f)+1)
tl=len(t_out)
s =np.zeros(tl, dtype=np.float_)

for i in range(n):
	for j in range(tl):
		if(t_out[j]>=x[i] and t_out[j]<x[i+1]):
			s[j]=( a[i]+_b[i]*(t_out[j]-x[i])+_c[i]*(t_out[j]-x[i])**2+_d[i]*(t_out[j]-x[i])**3)
s[-1]=a[-1]+_b[-1]*(t_out[-1]-x[-1]+_c[-1]*(t_out[-1]-x[-1])**2+_d[-1]*(t_out[-1]-x[-1])**3)


plt.plot(t_out, s, 'b-')
plt.plot(x,a,'ro')
plt.show()


