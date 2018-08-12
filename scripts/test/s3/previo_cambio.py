# 0.3.2
# Get jerk value
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
	q0=path_simple_cub_v0(_points[0],_time,_f)
	q1=path_simple_cub_v0(_points[1],_time,_f)
	q2=path_simple_cub_v0(_points[2],_time,_f)
	q3=path_simple_cub_v0(_points[3],_time,_f)
	q4=path_simple_cub_v0(_points[4],_time,_f)
	q5=path_simple_cub_v0(_points[5],_time,_f)
	q6=path_simple_cub_v0(_points[6],_time,_f)
	print q6
	q= np.array([q0,q1,q2,q3,q4,q5,q6])
	ext = len(q0)
	if(p):
		print "Knots en posicion generados.",ext
	return q, ext

def generate_vel(_j,_f,p=True):
	ext = len(_j[0,:])
	v0=np.zeros(ext)
	v1=np.zeros(ext)
	v2=np.zeros(ext)
	v3=np.zeros(ext)
	v4=np.zeros(ext)
	v5=np.zeros(ext)
	v6=np.zeros(ext)
	for n in range(ext-1):
		v0[n]=((_j[0][n+1]-_j[0][n])*_f)
		v1[n]=((_j[1][n+1]-_j[1][n])*_f)
		v2[n]=((_j[2][n+1]-_j[2][n])*_f)
		v3[n]=((_j[3][n+1]-_j[3][n])*_f)
		v4[n]=((_j[4][n+1]-_j[4][n])*_f)
		v5[n]=((_j[5][n+1]-_j[5][n])*_f)
		v6[n]=((_j[6][n+1]-_j[6][n])*_f)
	v0[-1]=v0[-2]
	v1[-1]=v1[-2]
	v2[-1]=v2[-2]
	v3[-1]=v3[-2]
	v4[-1]=v4[-2]
	v5[-1]=v5[-2]
	v6[-1]=v6[-2]
	v= np.array([v0,v1,v2,v3,v4,v5,v6])
	if(p):
		print "Knots en velocidad generados: ",ext
	return v,ext

def generate_acel(_v,_f, p=True):
	ext = len(_v[0])
	a0=np.zeros(ext)
	a1=np.zeros(ext)
	a2=np.zeros(ext)
	a3=np.zeros(ext)
	a4=np.zeros(ext)
	a5=np.zeros(ext)
	a6=np.zeros(ext)
	for n in range(ext-1):
		a0[n]=(_v[0][n+1]-_v[0][n])*_f
		a1[n]=(_v[1][n+1]-_v[1][n])*_f
		a2[n]=(_v[2][n+1]-_v[2][n])*_f
		a3[n]=(_v[3][n+1]-_v[3][n])*_f
		a4[n]=(_v[4][n+1]-_v[4][n])*_f
		a5[n]=(_v[5][n+1]-_v[5][n])*_f
		a6[n]=(_v[6][n+1]-_v[6][n])*_f
	a0[-2]=a0[-3]
	a1[-2]=a1[-3]
	a2[-2]=a2[-3]
	a3[-2]=a3[-3]
	a4[-2]=a4[-3]
	a5[-2]=a5[-3]
	a6[-2]=a6[-3]

	a0[-1]=a0[2]
	a1[-1]=a1[2]
	a2[-1]=a2[2]
	a3[-1]=a3[2]
	a4[-1]=a4[2]
	a5[-1]=a5[2]
	a6[-1]=a6[2]
	a= np.array([a0,a1,a2,a3,a4,a5,a6])
	if(p):
		print "Knots en aceleracion generados: ",ext
	return a,ext

def generate_jerk(_a,_f,p=True):
	ext = len(_a[0])
	jk0=np.zeros(ext)
	jk1=np.zeros(ext)
	jk2=np.zeros(ext)
	jk3=np.zeros(ext)
	jk4=np.zeros(ext)
	jk5=np.zeros(ext)
	jk6=np.zeros(ext)

	for n in range(ext-1):
		jk0[n]=((_a[0][n+1]-_a[0][n])*_f)
		jk1[n]=((_a[1][n+1]-_a[1][n])*_f)
		jk2[n]=((_a[2][n+1]-_a[2][n])*_f)
		jk3[n]=((_a[3][n+1]-_a[3][n])*_f)
		jk4[n]=((_a[4][n+1]-_a[4][n])*_f)
		jk5[n]=((_a[5][n+1]-_a[5][n])*_f)
		jk6[n]=((_a[6][n+1]-_a[6][n])*_f)

	jk0[-3]=jk0[-4]
	jk1[-3]=jk1[-4]
	jk2[-3]=jk2[-4]
	jk3[-3]=jk3[-4]
	jk4[-3]=jk4[-4]
	jk5[-3]=jk5[-4]
	jk6[-3]=jk6[-4]

	jk0[-2]=jk0[-3]
	jk1[-2]=jk1[-3]
	jk2[-2]=jk2[-3]
	jk3[-2]=jk3[-3]
	jk4[-2]=jk4[-3]
	jk5[-2]=jk5[-3]
	jk6[-2]=jk6[-3]

	jk0[-1]=jk0[-2]
	jk1[-1]=jk1[-2]
	jk2[-1]=jk2[-2]
	jk3[-1]=jk3[-2]
	jk4[-1]=jk4[-2]
	jk5[-1]=jk5[-2]
	jk6[-1]=jk6[-2]
	ext= len(jk0)

	a_jk0=get_area(jk0,_f)
	a_jk1=get_area(jk1,_f)
	a_jk2=get_area(jk2,_f)
	a_jk3=get_area(jk3,_f)
	a_jk4=get_area(jk4,_f)
	a_jk5=get_area(jk5,_f)
	a_jk6=get_area(jk6,_f)

	a=a_jk0+a_jk1+a_jk2+a_jk3+a_jk4+a_jk5+a_jk6
	ind=sqrt(a)
	jk= [jk0,jk1,jk2,jk3,jk4,jk5,jk6]
	if(p):
		print "Knots en jerk generados.",ext
	return jk, ind,ext

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
	s =np.zeros(tl, dtype=np.float_)

	if(jerk_value):
		for i in range(n):
			for j in range(tl):
				if(t_out[j]>=x[i] and t_out[j]<x[i+1]):
					s[j]=6*_d[i]
		s[-1]=6*_d[-1]
	else:
		for i in range(n):
			for j in range(tl):
				if(t_out[j]>=x[i] and t_out[j]<x[i+1]):
					s[j]=( a[i]+_b[i]*(t_out[j]-x[i])+_c[i]*(t_out[j]-x[i])**2+_d[i]*(t_out[j]-x[i])**3)
		s[-1]=a[-1]+_b[-1]*(t_out[-1]-x[-1])+_c[-1]*(t_out[-1]-x[-1])**2+_d[-1]*(t_out[-1]-x[-1])**3)
	return s

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

def value_sum_jerk(_points,_time,_f):
	jk0=path_simple_cub_v0(_points[0],_time,_f,jerk_value=True)
	jk1=path_simple_cub_v0(_points[1],_time,_f,jerk_value=True)
	jk2=path_simple_cub_v0(_points[2],_time,_f,jerk_value=True)
	jk3=path_simple_cub_v0(_points[3],_time,_f,jerk_value=True)
	jk4=path_simple_cub_v0(_points[4],_time,_f,jerk_value=True)
	jk5=path_simple_cub_v0(_points[5],_time,_f,jerk_value=True)
	jk6=path_simple_cub_v0(_points[6],_time,_f,jerk_value=True)
	print jk6
	ext= len(jk0)
	a_jk0=get_area(jk0,_f)
	a_jk1=get_area(jk1,_f)
	a_jk2=get_area(jk2,_f)
	a_jk3=get_area(jk3,_f)
	a_jk4=get_area(jk4,_f)
	a_jk5=get_area(jk5,_f)
	a_jk6=get_area(jk6,_f)

	a=a_jk0+a_jk1+a_jk2+a_jk3+a_jk4+a_jk5+a_jk6

	ind=sqrt(a)
	return ind,ext

class Opt_avalos():

	def __init__(self,_q,_f):
		self.q=_q
		self.f=_f
		g=np.array([0.0])
		x0 = np.array([1.0])
		res = minimize(self.hola, x0, method='nelder-mead',options={'xtol': 1e-1, 'disp': True})
		print "value"
		print res.x
		print res

	def hola(self,k):
		print k
		[t_0,t_rec]=min_time(self.q)
		t=k*t_0
		[v_jk,ext]=value_sum_jerk(self.q,t,self.f)
		v_t=round(6*(ext/float(self.f)),2)
		ecu=v_jk+v_t
		print "Cost:"
		print ecu
		print "Jerk value:"
		print v_jk
		return ecu

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
