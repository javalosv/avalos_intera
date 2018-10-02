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

def ik_service_client_full(_p):
	_limb = intera_interface.Limb('right')
	ns = "ExternalTools/right/PositionKinematicsNode/IKService"
	iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
	ikreq = SolvePositionIKRequest()
	hdr = Header(stamp=rospy.Time.now(), frame_id='base')
	poses = {
		'right': PoseStamped(
			header=hdr,
			pose=Pose(
				position=Point(
					x=_p[0],
					y=_p[1],
					z=_p[2],
				),
				orientation=Quaternion(
					x=_p[3],
					y=_p[4],
					z=_p[5],
					w=_p[6],
				),
			),
		),
	}
	# Add desired pose for inverse kinematics
	ikreq.pose_stamp.append(poses["right"])
	# Request inverse kinematics from base to "right_hand" link
	ikreq.tip_names.append('right_hand')


	try:
		rospy.wait_for_service(ns, 5.0)
		resp = iksvc(ikreq)
	except (rospy.ServiceException, rospy.ROSException), e:
		rospy.logerr("Service call failed: %s" % (e,))
		return False

	# Check if result valid, and type of seed ultimately used to get solution
	if (resp.result_type[0] > 0):
		# Format solution into Limb API-compatible dictionary
		limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
		rospy.loginfo("Solucion IK ok.")
		_limb.move_to_joint_positions(limb_joints)
		q=np.array([resp.joints[0].position[0],resp.joints[0].position[1],resp.joints[0].position[2],resp.joints[0].position[3],resp.joints[0].position[4],resp.joints[0].position[5],resp.joints[0].position[6]])
		print q
		return True , q
	else:
		rospy.logerr("INVALID POSE - No Valid Joint Solution Found.")
		rospy.logerr("Result Error %d", resp.result_type[0])
		q=np.array([0,0,0,0,0,0,0])
		return False, q

def get_area(_vector,_f):
	_v=np.power(_vector,2)
	k=np.sum(_v)-0.5*(_v[0]+_v[-1])
	area=k/float(_f)
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

def path_simple_cub_get_jerk(_point,_time,_f):
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

	t_out=np.linspace(x[0], x[-1], int((x[-1]-x[0])*f)+1)
	tl=len(t_out)
	y =np.zeros(tl, dtype=np.float_)
	for i in range(n):
		for j in range(tl):
			if(t_out[j]>=x[i] and t_out[j]<x[i+1]):
				y[j]=6*_d[i]
	k1=int((h[0])*f)
	k2=int((h[-1])*f+1)

	s_v=_b[1]
	s_ac=2*_c[1]
	s_y=6*_d[1]
	h_e=h[-1]

	# Spline 7 grade begin
	a00 =(10*s_v)/h[0]**6 - (2*s_ac)/h[0]**5 + s_y/(6*h[0]**4) + (20*(a[0]-a[1]))/h[0]**7
	a01 =(13*s_ac)/(2*h[0]**4) - (34*s_v)/h[0]**5 - s_y/(2*h[0]**3) - (70*(a[0]-a[1]))/h[0]**6
	a02 =(39*s_v)/h[0]**4 - (7*s_ac)/h[0]**3 + s_y/(2*h[0]**2) + (84*(a[0]-a[1]))/h[0]**5
	a03 =(5*s_ac)/(2*h[0]**2) - (15*s_v)/h[0]**3 - s_y/(6*h[0]) - (35*(a[0]-a[1]))/h[0]**4
	for j in range(k1):
	    y[j]=210*a00*(j*0.01)**4+120*a01*(j*0.01)**3+60*a02*(j*0.01)**2+24*a03*(j*0.01)**1
	#  Spline 7 grade end
	a7=a[-2]
	a6=_b[-1]
	a5= _c[i]
	a4= -_d[i]
	h_e=h[-1]
	p_e=a[-1]

	ak0 = (2*(2*a5 + 6*a4*h_e))/h_e**5 - a4/h_e**4 - (10*(3*a4*h_e**2 + 2*a5*h_e + a6))/h_e**6 + (20*(a4*h_e**3 + a5*h_e**2 + a6*h_e + a7 - p_e))/h_e**7
	ak1 = (3*a4)/h_e**3 - (13*(2*a5 + 6*a4*h_e))/(2*h_e**4) + (34*(3*a4*h_e**2 + 2*a5*h_e + a6))/h_e**5 - (70*(a4*h_e**3 + a5*h_e**2 + a6*h_e + a7 - p_e))/h_e**6
	ak2 = (7*(2*a5 + 6*a4*h_e))/h_e**3 - (3*a4)/h_e**2 - (39*(3*a4*h_e**2 + 2*a5*h_e + a6))/h_e**4 + (84*(a4*h_e**3 + a5*h_e**2 + a6*h_e + a7 - p_e))/h_e**5
	ak3 = a4/h_e - (5*(2*a5 + 6*a4*h_e))/(2*h_e**2) + (15*(3*a4*h_e**2 + 2*a5*h_e + a6))/h_e**3 - (35*(a4*h_e**3 + a5*h_e**2 + a6*h_e + a7 - p_e))/h_e**4

	for j in range(k2):
	    y[-k2+j]=210*ak0*(j*0.01)**4+120*ak1*(j*0.01)**3+60*ak2*(j*0.01)**2+24*ak3*(j*0.01)**1+6*a4

	return y

def path_simple_cub_v0(_point,_time,_f):
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

	for i in range(n):
		for j in range(tl):
			if(t_out[j]>=x[i] and t_out[j]<x[i+1]):
				p[j]=( a[i]+_b[i]*(t_out[j]-x[i])+_c[i]*(t_out[j]-x[i])**2+_d[i]*(t_out[j]-x[i])**3)
				v[j]=_b[i]+2*_c[i]*(t_out[j]-x[i])+3*_d[i]*(t_out[j]-x[i])**2
				ac[j]=2*_c[i]+6*_d[i]*(t_out[j]-x[i])
				y[j]=6*_d[i]
	k1=int((h[0])*f)
	k2=int((h[-1])*f+1)

	s_v=v[k1]
	s_ac=ac[k1]
	s_y=y[k1]
	h_0=h[0]
	h_e=h[-1]

	# Spline 7 grade begin
	a00 =(10*s_v)/h_0**6 - (2*s_ac)/h_0**5 + s_y/(6*h_0**4) + (20*(a[0]-a[1]))/h_0**7
	a01 =(13*s_ac)/(2*h_0**4) - (34*s_v)/h_0**5 - s_y/(2*h_0**3) - (70*(a[0]-a[1]))/h_0**6
	a02 =(39*s_v)/h_0**4 - (7*s_ac)/h_0**3 + s_y/(2*h_0**2) + (84*(a[0]-a[1]))/h_0**5
	a03 =(5*s_ac)/(2*h_0**2) - (15*s_v)/h_0**3 - s_y/(6*h_0) - (35*(a[0]-a[1]))/h_0**4
	for j in range(k1):
	    p[j]=a00*(j*0.01)**7+a01*(j*0.01)**6+a02*(j*0.01)**5+a03*(j*0.01)**4+a[0]
	    v[j]=7*a00*(j*0.01)**6+6*a01*(j*0.01)**5+5*a02*(j*0.01)**4+4*a03*(j*0.01)**3
	    ac[j]=42*a00*(j*0.01)**5+30*a01*(j*0.01)**4+20*a02*(j*0.01)**3+12*a03*(j*0.01)**2
	    y[j]=210*a00*(j*0.01)**4+120*a01*(j*0.01)**3+60*a02*(j*0.01)**2+24*a03*(j*0.01)**1

	#  Spline 7 grade end
	a7=a[-2]
	a6=v[-k2]
	a5= ac[-k2]/2
	a4= -y[-k2]/6
	h_e=h[-1]
	p_e=a[-1]

	ak0 = (2*(2*a5 + 6*a4*h_e))/h_e**5 - a4/h_e**4 - (10*(3*a4*h_e**2 + 2*a5*h_e + a6))/h_e**6 + (20*(a4*h_e**3 + a5*h_e**2 + a6*h_e + a7 - p_e))/h_e**7
	ak1 = (3*a4)/h_e**3 - (13*(2*a5 + 6*a4*h_e))/(2*h_e**4) + (34*(3*a4*h_e**2 + 2*a5*h_e + a6))/h_e**5 - (70*(a4*h_e**3 + a5*h_e**2 + a6*h_e + a7 - p_e))/h_e**6
	ak2 = (7*(2*a5 + 6*a4*h_e))/h_e**3 - (3*a4)/h_e**2 - (39*(3*a4*h_e**2 + 2*a5*h_e + a6))/h_e**4 + (84*(a4*h_e**3 + a5*h_e**2 + a6*h_e + a7 - p_e))/h_e**5
	ak3 = a4/h_e - (5*(2*a5 + 6*a4*h_e))/(2*h_e**2) + (15*(3*a4*h_e**2 + 2*a5*h_e + a6))/h_e**3 - (35*(a4*h_e**3 + a5*h_e**2 + a6*h_e + a7 - p_e))/h_e**4

	for j in range(k2):
	    p[-k2+j]=ak0*(j*0.01)**7+ak1*(j*0.01)**6+ak2*(j*0.01)**5+ak3*(j*0.01)**4+a4*(j*0.01)**3+a5*(j*0.01)**2+a6*(j*0.01)+a7
	    v[-k2+j]=7*ak0*(j*0.01)**6+6*ak1*(j*0.01)**5+5*ak2*(j*0.01)**4+4*ak3*(j*0.01)**3+3*a4*(j*0.01)**2+2*a5*(j*0.01)+a6
	    ac[-k2+j]=42*ak0*(j*0.01)**5+30*ak1*(j*0.01)**4+20*ak2*(j*0.01)**3+12*ak3*(j*0.01)**2+6*a4*(j*0.01)+2*a5
	    y[-k2+j]=210*ak0*(j*0.01)**4+120*ak1*(j*0.01)**3+60*ak2*(j*0.01)**2+24*ak3*(j*0.01)**1+6*a4

	return p,v,ac,y,tl

	# Se determina el minimo tiempo para ejecutar el movimiento

def min_time(_q):
	vel_lim=[1.74, 1.328, 1.957, 1.957, 3.485, 3.485, 4.545]
	# Es un concepto de seguridad para las pruebas.
	v_factor=0.9
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
		[self.min_time,self.t_rec]=min_time(self.q)
		self.l=len(self.min_time)-1
		self.delta_t=np.ones(self.l)
		self.v_time=self.min_time
		print "Min_time:",self.min_time
		x0 = np.ones(1)
		bnds=[(1,None)]
		print "x0:",len(x0)
		print "b:",len(bnds)
		print "Working in solution alfa=",str(_alfa)
		#self.res = minimize(self.costo, x0,method='L-BFGS-B', bounds=bnds ,options={'ftol': 2e-3, 'disp': False})
		myfactr = 1e18* np.finfo(float).eps
		print "myfactr:",myfactr
		self.res = minimize(self.costo, x0, method='nelder-mead',options={'ftol' : myfactr ,'disp': False})

	def costo(self,k):
		#print "k_value:",k
		self.t=k*self.v_time
		#print "t", self.t 
		[self.value_jk,ext]=self.value_sum_jerk(self.q,self.t,self.f)
		# Funcion Costo
		self.value_t=round(6*(ext/float(self.f)),2)
		ecu=self.alfa*self.value_t+(1-self.alfa)*self.value_jk
		print "ecu:", k, ecu
		return ecu
	def value_sum_jerk(self,_points,_time,_f):
		jk0=path_simple_cub_get_jerk(_points[0],_time,_f)
		jk1=path_simple_cub_get_jerk(_points[1],_time,_f)
		jk2=path_simple_cub_get_jerk(_points[2],_time,_f)
		jk3=path_simple_cub_get_jerk(_points[3],_time,_f)
		jk4=path_simple_cub_get_jerk(_points[4],_time,_f)
		jk5=path_simple_cub_get_jerk(_points[5],_time,_f)
		jk6=path_simple_cub_get_jerk(_points[6],_time,_f)
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
	def full_time(self):
		return self.t
	def result(self):
		return self.res.x
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
		self.tmp=np.zeros(self.l)
		bnds = ()
		for i in range(self.l):
			bnds+=((1,None),)
			self.delta_t[i]=self.min_time[i+1]-self.min_time[i]
		x0 = np.ones(self.l)
		print "Working in solution alfa=",str(_alfa)
		#print bnds
		myfactr = 5e-3
		self.res = minimize(self.costo, x0,method='L-BFGS-B', bounds=bnds ,options={'ftol' : myfactr ,'disp': False, 'eps': 0.0002})
		self.tmp=self.res.x*self.delta_t
		self.v_time=np.append([0],self.tmp.cumsum())
		[self.value_jk,ext]=self.value_sum_jerk(self.q,self.v_time,self.f)
		# Funcion Costo
		self.value_t=round(6*(ext/float(self.f)),2)

	def costo(self,k):
		k=k*self.delta_t
		# Funcion Costo
		[value_jk,ext]=self.value_sum_jerk(self.q,np.append([0],k.cumsum()),self.f)
		value_t=round(6*(ext/float(self.f)),2)
		ecu=self.alfa*value_t+(1-self.alfa)*value_jk
		print "ecu:", k, ecu
		return ecu
	def value_sum_jerk(self,_points,_time,_f):
		jk0=path_simple_cub_get_jerk(_points[0],_time,_f)
		jk1=path_simple_cub_get_jerk(_points[1],_time,_f)
		jk2=path_simple_cub_get_jerk(_points[2],_time,_f)
		jk3=path_simple_cub_get_jerk(_points[3],_time,_f)
		jk4=path_simple_cub_get_jerk(_points[4],_time,_f)
		jk5=path_simple_cub_get_jerk(_points[5],_time,_f)
		jk6=path_simple_cub_get_jerk(_points[6],_time,_f)
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

	def full_time(self):
		return self.v_time
	def result(self):
		return self.res.x
	def value_time(self):
		return self.value_t
	def minimal_time(self):
		return self.min_time
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
