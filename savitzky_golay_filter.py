import numpy as np
from math import sqrt

def generate2d(points, degree):
	if points % 2 == 0:
		raise ValueError("Cannot convolve with an even number of points in one axis")
	#Fint the central point in each axis
	central = (points-1)//2
	#z contains each point, mapped to a point where the center of all the points is (0, 0)
	z = []
	for i in range(points):
		z.append(i-central)
	#J is a matrix, which when multiplied with a vector containing each cooefficient (a0, a1, a2, ...),
	# generates the height.
	#Therefore, if h = a[0] + u*a[1] + u^2*a[2] + ... + u^(degree)*a[degree] + v*a[degree+1] + u*v*a[degree+2] + ...
	# and h = Ja, then J = [
	# 	[1, u, u^2, ..., v, u*v, u^2*v, ...]
	# ]
	#As we have points*points amount of total points, there will be 
	J = np.zeros((points*points, ((degree+1)*(degree+2))//2), np.float)
	for i in range(len(J)):
		#u is the row index, and as we are going row-major,
		# this is the floored devision of the current index by the length of a row.
		#And that makes v, the column index, the index modulus the length of a row.
		u = z[i//points]
		v = z[i%points]
		#cu and cv are the current powers of u and v respectivally. They both start at 0.
		cu = 0
		cv = 0
		for j in range(len(J[i])):
			#Set the current place to u^cu * v^cv
			J[i][j] = u**cu * v**cv
			#Increment cu
			cu += 1
			#But if we have gone over the intended order, reset cu, and increment cv
			if cv + cu > degree:
				cu = 0
				cv += 1
	#JT is the transpose of J, and C is the pseudo-inverse of J.
	JT = np.transpose(J)
	C = np.matmul(np.linalg.inv(np.matmul(JT, J)), JT)
	return C

def termsWithThesePowers(up, vp, degree):
	out = []
	cu = 0
	cv = 0
	for j in range(((degree+1)*(degree+2))//2):
		#u**cu * v**cv
		if cv == vp and cu == up:
			out.append(j)
		cu += 1
		if cv + cu > degree:
			cu = 0
			cv += 1
		if cu > up and cv > vp:
			break
	return out
	
def makeKernel(matrix, selection, points):
	l = len(matrix[0])
	kernel = np.zeros((points, points), np.float)
	for s in selection:
		for i in range(l):
			kernel[i//points][i%points] += matrix[s][i]
	return kernel

def makeKernelEPIC(matrix, selections, points):
	l = len(matrix[0])
	kernel = np.zeros((points, points), np.float)
	for g in selections:
		for s in g[0]:
			for i in range(l):
				kernel[i//points][i%points] += matrix[s][i] * g[1]
	return kernel

def shiftKernel(kernel, amount, shiftJ):
	size = len(kernel) + abs(amount)*2
	newKernel = np.zeros((size, size), np.float)
	copyRangeJ = range(abs(amount), size-abs(amount))
	if amount < 0:
		copyRangeI = range(0, len(kernel))
	else:
		copyRangeI = range(size-len(kernel), size)
	if shiftJ:
		copyRangeI, copyRangeJ = (copyRangeJ, copyRangeI)
	i = 0
	for newI in copyRangeI:
		j = 0
		for newJ in copyRangeJ:
			newKernel[newI][newJ] = kernel[i][j]
			j += 1
		i += 1
	return newKernel

def makeXGradientKernel(window, degree):
	return makeKernel(generate2d(window, degree), termsWithThesePowers(0, 1, degree), window)
	
def makeYGradientKernel(window, degree):
	return makeKernel(generate2d(window, degree), termsWithThesePowers(1, 0, degree), window)

def makeXGradientKernelEdgeBelow(window, degree):
	return shiftKernel(makeKernelEPIC(generate2d(window, degree), [
		(termsWithThesePowers(0, 1, degree), 1),
		(termsWithThesePowers(1, 1, degree), (window-1)/2),
	], window), -(window-1)//2, False)
	
def makeXGradientKernelEdgeAbove(window, degree):
	return shiftKernel(makeKernelEPIC(generate2d(window, degree), [
		(termsWithThesePowers(0, 1, degree), 1),
		(termsWithThesePowers(1, 1, degree), -(window-1)/2),
	], window), (window-1)//2, False)
	
def makeYGradientKernelEdgeRight(window, degree):
	return shiftKernel(makeKernelEPIC(generate2d(window, degree), [
		(termsWithThesePowers(1, 0, degree), 1),
		(termsWithThesePowers(1, 1, degree), (window-1)/2),
	], window), -(window-1)//2, True)
	
def makeYGradientKernelEdgeLeft(window, degree):
	return shiftKernel(makeKernelEPIC(generate2d(window, degree), [
		(termsWithThesePowers(1, 0, degree), 1),
		(termsWithThesePowers(1, 1, degree), -(window-1)/2),
	], window), (window-1)//2, True)
	
def P(n, k):
	if k > n:
		return 0
	if k == 0:
		return 1
	k = n - k + 1
	r = k
	k += 1
	while k <= n:
		r *= k
		k += 1
	return r

def makeIt(window, degree, x, y, dx, dy):
	selections = []
	central = (window-1)//2
	u = y - central
	v = x - central
	
	cu = 0
	cv = 0
	for j in range(((degree+1)*(degree+2))//2):
		#u**cu * v**cv term,
		# dxth derivative with respect to v:
		#  u**cu * cv*(cv-1)*...*(cv-dx+1)*v**(cv-dx)
		# Then, the dyth derivative of that, with respect to u, is:
		#  cu*(cu-1)*...*(cu-dy+1)*u**(cu-dy) * cv*(cv-1)*...*(cv-dx+1)*v**(cv-dx)
		#  = cu!/(cu-dy)!*u**(cu-dy) * cv!/(cv-dx)!*v**(cv-dx)
		#  = P(cu, dy)*u**(cu-dy) * P(cv, dx)*v**(cv-dx)
		#  = P(cu, dy) * P(cv, dx) * v**(cv-dx) * u**(cu-dy)
		mul = P(cu, dy)*P(cv, dx)
		if mul != 0:
			#print("d^"+str(dy)+"u/dx^"+str(dy)+"(d^"+str(dx)+"v/dx^"+str(dx)+"(u^"+str(cu)+"v^"+str(cv)+"x))="+str(mul)+"u^"+str(cu-dy)+"v^"+str(cv-dx)+"x (u="+str(u)+", v="+str(v)+")")
			mul *= v**(cv-dx) * u**(cu-dy)
			if mul != 0:
				selections.append(([j], mul))
		#else:
			#print("d^"+str(dy)+"u/dx^"+str(dy)+"(d^"+str(dx)+"v/dx^"+str(dx)+"(u^"+str(cu)+"v^"+str(cv)+"x))=0")
		cu += 1
		if cv + cu > degree:
			cu = 0
			cv += 1
	
	return shiftKernel(shiftKernel(makeKernelEPIC(generate2d(window, degree), selections, window), central-y, False), central-x, True)
