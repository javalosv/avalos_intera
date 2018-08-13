# 0.3.4
from __future__ import division
import argparse
import rospy
import intera_interface
import intera_external_devices
import time
import numpy as np
from math import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import minimize
from intera_core_msgs.msg import JointCommand
from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.interpolate import interp1d
from geometry_msgs.msg import (
	PoseStamped,
	Pose,
	Point,
	Quaternion,
)
from std_msgs.msg import Header
from sensor_msgs.msg import JointState
from intera_core_msgs.srv import (
	SolvePositionIK,
	SolvePositionIKRequest,
)

def get_area(_vector,_f):
	h=1.0/float(_f)
	_v=np.power(_vector,2)
	k=np.sum(_v)
	k=k-0.5*(_v[0]+_v[-1])
	area=k*h
	return area

def save_matrix(_j,_name,_f):
	file2write=open(_name,'w')
	l=len(_j[0][:])
	time=np.linspace(0, (l-1)/float(_f), num=l)
	for n in range(l):
		file2write.write(str(time[n])+' , '+str(_j[0][n])+' , '+str(_j[1][n])+' , '+str(_j[2][n])+' , '+str(_j[3][n])+' , '+ str(_j[4][n])+' , '+str(_j[5][n])+' , '+str(_j[6][n])+'\n')
	file2write.close()
	print "save data en",_name
	return True

def generate_path_cub(_points,_time,_f,p=True):
	[q0,v0,a0,y0,l]=path_simple_cub_v0(_points[0],_time,_f)
	[q1,v1,a1,y1,l]=path_simple_cub_v0(_points[1],_time,_f)
	[q2,v2,a2,y2,l]=path_simple_cub_v0(_points[2],_time,_f)
	[q3,v3,a3,y3,l]=path_simple_cub_v0(_points[3],_time,_f)
	[q4,v4,a4,y4,l]=path_simple_cub_v0(_points[4],_time,_f)
	[q5,v5,a5,y5,l]=path_simple_cub_v0(_points[5],_time,_f)
	[q6,v6,a6,y6,l]=path_simple_cub_v0(_points[6],_time,_f)
	q= np.array([q0,q1,q2,q3,q4,q5,q6])
	v= np.array([v0,v1,v2,v3,v4,v5,v6])
	a= np.array([a0,a1,a2,a3,a4,a5,a6])
	y= np.array([y0,y1,y2,y3,y4,y5,y6])
	ext = l
	if(p):
		print "Knots en posicion generados.",ext
	return q,v,a,y

def path_simple_cub_v0(_point,_time,_f,jerk_value=False):
	x=_time
	a=_point
	f=_f
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
	sA = np.zeros(shape=(n+1,n+1), dtype=np.float_)
	for i in range(n-1) :
		for j in range(n-1) :
			if i is j:
				sA[i+1][i+1]=2*(h[i]+h[i+1])
				sA[i+1][i]=h[i]
				sA[i][i+1]=h[i]
	sA[0][0]=2*h[0]
	sA[-1][-1]=2*h[-1]
	sA[-1][-2]=h[-1]
	sA[-2][-1]=h[-1]

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
	p =np.zeros(tl, dtype=np.float_)
	v =np.zeros(tl, dtype=np.float_)
	ac =np.zeros(tl, dtype=np.float_)
	y =np.zeros(tl, dtype=np.float_)
	if(jerk_value):
		for i in range(n):
			for j in range(tl):
				if(t_out[j]>=x[i] and t_out[j]<x[i+1]):
					y[j]=6*_d[i]
		y[-1]=y[-2]
		return y
	else:
		for i in range(n):
			for j in range(tl):
				if(t_out[j]>=x[i] and t_out[j]<x[i+1]):
					p[j]=( a[i]+_b[i]*(t_out[j]-x[i])+_c[i]*(t_out[j]-x[i])**2+_d[i]*(t_out[j]-x[i])**3)
					v[j]=_b[i]+2*_c[i]*(t_out[j]-x[i])+3*_d[i]*(t_out[j]-x[i])**2
					ac[j]=2*_c[i]+6*_d[i]*(t_out[j]-x[i])
					y[j]=6*_d[i]
		p[-1]=a[-1]
		v[-1]=0
		ac[-1]=ac[-2] # Aceleracion misma letra que a como polinomio
		y[-1]=y[-2]
		return p,v,ac,y,tl

	# Se determina el minimo tiempo para ejecutar el movimiento

def min_time(_q):
	vel_lim=[1.74, 1.328, 1.957, 1.957, 3.485, 3.485, 4.545]
	# Luego de pruebas es el valor minimo para las pruebas. Es un concepto de seguridad para las pruebas.
	v_factor=1
	N=len(vel_lim)
	k=len(_q[0])
	t_min=np.zeros(k, dtype=np.float_)
	t_tmp=np.zeros(N, dtype=np.float_)
	for i in range (k-1):
		for j in range (N):
			t_tmp[j]= abs((_q[j,i+1]-_q[j,i])/((v_factor)*vel_lim[j]))
		w=np.amax(t_tmp)# Se asume t[0]=0
		t_min[i+1]=w+t_min[i]
	return t_min, sum(t_min)

class Opt_1_avalos():
	def __init__(self,_q,_f,_alfa):
		self.q=_q
		self.f=_f
		self.alfa=_alfa
		[self.t_v,self.t_rec]=min_time(self.q)
		g=np.array([0.0])
		x0 = np.array([1.0])
		self.res = minimize(self.costo, x0, method='nelder-mead',options={'xtol': 1e-1, 'disp': False})
	def costo(self,k):
		self.t=k*self.t_v
		[self.value_jk,ext]=self.value_sum_jerk(self.q,self.t,self.f)
		self.value_t=round(6*(ext/float(self.f)),2)
		ecu=self.alfa*self.value_t+(1-self.alfa)*self.value_jk
		return ecu
	def value_sum_jerk(self,_points,_time,_f):
		jk0=path_simple_cub_v0(_points[0],_time,_f,jerk_value=True)
		jk1=path_simple_cub_v0(_points[1],_time,_f,jerk_value=True)
		jk2=path_simple_cub_v0(_points[2],_time,_f,jerk_value=True)
		jk3=path_simple_cub_v0(_points[3],_time,_f,jerk_value=True)
		jk4=path_simple_cub_v0(_points[4],_time,_f,jerk_value=True)
		jk5=path_simple_cub_v0(_points[5],_time,_f,jerk_value=True)
		jk6=path_simple_cub_v0(_points[6],_time,_f,jerk_value=True)
		ext= len(jk0)
		a_jk0=get_area(jk0,_f)
		a_jk1=get_area(jk1,_f)
		a_jk2=get_area(jk2,_f)
		a_jk3=get_area(jk3,_f)
		a_jk4=get_area(jk4,_f)
		a_jk5=get_area(jk5,_f)
		a_jk6=get_area(jk6,_f)
		value_jk=a_jk0+a_jk1+a_jk2+a_jk3+a_jk4+a_jk5+a_jk6
		ind=sqrt(value_jk)
		return ind,ext
	def value(self):
		return self.t
	def result(self):
		return self.res
	def value_time(self):
		return self.value_t
	def value_jerk(self):
		return self.value_jk

class Opt_2_avalos():
	def __init__(self,_q,_f,_alfa):
		self.q=_q
		self.f=_f
		self.alfa=_alfa
		[self.min_time,self.t_rec]=min_time(self.q)
		self.l=len(self.min_time)-1
		self.delta_t=np.ones(self.l)
		self.v_time=self.min_time
		for i in range(self.l):
			tmp=self.min_time[i+1]-self.min_time[i]
			self.delta_t[i]=tmp
		x0 = np.ones(self.l)
		print "Working in solution"
		bnds = ((1, None),(1, None), (1, None), (1, None), (1, None), (1, None), (1, None), (1, None), (1, None), (1, None))
		self.res = minimize(self.costo, x0,method='SLSQP', bounds=bnds, tol=0.01,options={ 'disp': False})
	def costo(self,k):
		t=k*self.delta_t
		for i in range(self.l):
			tmp=self.v_time[i]+t[i]
			self.v_time[i+1]=tmp
		[self.value_jk,ext]=self.value_sum_jerk(self.q,self.v_time,self.f)
		# Funcion Costo
		self.value_t=round((ext/float(self.f))**2,2)
		ecu=self.alfa*self.value_t+(1-self.alfa)*self.value_jk
		return ecu
	def value_sum_jerk(self,_points,_time,_f):
		jk0=path_simple_cub_v0(_points[0],_time,_f,jerk_value=True)
		jk1=path_simple_cub_v0(_points[1],_time,_f,jerk_value=True)
		jk2=path_simple_cub_v0(_points[2],_time,_f,jerk_value=True)
		jk3=path_simple_cub_v0(_points[3],_time,_f,jerk_value=True)
		jk4=path_simple_cub_v0(_points[4],_time,_f,jerk_value=True)
		jk5=path_simple_cub_v0(_points[5],_time,_f,jerk_value=True)
		jk6=path_simple_cub_v0(_points[6],_time,_f,jerk_value=True)
		ext= len(jk0)
		a_jk0=get_area(jk0,_f)
		a_jk1=get_area(jk1,_f)
		a_jk2=get_area(jk2,_f)
		a_jk3=get_area(jk3,_f)
		a_jk4=get_area(jk4,_f)
		a_jk5=get_area(jk5,_f)
		a_jk6=get_area(jk6,_f)
		value_jk=a_jk0+a_jk1+a_jk2+a_jk3+a_jk4+a_jk5+a_jk6
		ind=sqrt(value_jk)
		return ind,ext
	def value(self):
		return self.v_time
	def result(self):
		return self.res
	def value_time(self):
		return self.value_t
	def value_jerk(self):
		return self.value_jk

class Data():
	def __init__(self):
		self.write=False
		rospy.Subscriber("/robot/joint_states", JointState, self.talker)
		print("Init bridge")
		rate = rospy.Rate(100) # 10hz

	def talker(self,data):
		if(data.name[0]=="head_pan"):
			self.position=data.position[1:7]# extrae solo 7
			if(self.write):
				_file=open(self.file,"a")
				_file.write(str(data.position[1])+","+str(data.position[2])+","+str(data.position[3])+","\
				+str(data.position[4])+","+str(data.position[5])+","+str(data.position[6])+","+str(data.position[7])+\
				","+str(data.velocity[1])+","+str(data.velocity[2])+","+str(data.velocity[3])+","\
				+str(data.velocity[4])+","+str(data.velocity[5])+","+str(data.velocity[6])+","+str(data.velocity[7])+"\n")
				_file.close()

	def actual_joint_position(self):
		return self.position

	def writeon(self,_text):
		self.write=True
		self.file=_text
		file=open(_text,"w")
		file.close()
		return True

	def writeoff(self):
		self.write=False
		return True
