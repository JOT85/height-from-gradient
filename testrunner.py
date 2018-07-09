import generater
import numpy as np
import math
import m
import testkernels as kernels
from plotheights import plot

def checkGenerator():
	m1, z1, dx1, dy1 = generater.generateSphereStuff(
		np.ndarray((256, 256)),
		np.ndarray((256, 256)),
		np.ndarray((256, 256)),
		59.9,
		100,
		100,
	)

	r2 = 59.9**2
	def f(x, y):
		z2 = r2 - (x-100)**2 - (y-100)**2
		if z2 < 0:
			return math.nan
		return math.sqrt(z2)

	m2, z2, dx2, dy2, _, _ , _ = generater.fromFunction(
		f,
		lambda x, y, z: (100-x)/z,
		lambda x, y, z: (100-y)/z,
		(0, 0),
		(256, 256),
	)

	if m1.width() != m2.width() or m1.height() != m2.height():
		raise RuntimeError("Mask dimensions not consistant")
	for x in range(m1.width()):
		for y in range(m1.height()):
			if m1.get(x, y) != m2.get(x, y):
				raise RuntimeError("Masks not equal")

	def checkEqual(a, b, label):
		if len(a) != len(b):
			raise RuntimeError(label + " dimensions not consistant")
		for i in range(len(a)):
			if a[i][0] != b[i][0]:
				raise RuntimeError(label + " not equal")

	checkEqual(z1, z2, "z")
	checkEqual(dx1, dx2, "dx")
	checkEqual(dy1, dy2, "dy")

	print("All good!!!")

def compareValues(a, b):
	if len(a) != len(b):
		raise RuntimeError("vectors must be the same size to compare")
	t = 0
	for i in range(len(a)):
		if (a[i]-b[i])**2 > 1000:
			#print(i, a[i], b[i])
			#print((a[i]-b[i])**2)
			t += (a[i]-b[i])**2
	return t / len(a)

def testFunction(f, start, end, dfdx=None, dfdy=None, noiseFunctions=(None, None), mask=None, step = 0.01, verbose=False, plotresults=False):
	if verbose: print("Testing...")
	if dfdx == None:
		dfdx = lambda x, y, z: (f(x+step, y) - f(x-step, y))/(2*step)
	if dfdy == None:
		dfdy = lambda x, y, z: (f(x, y+step) - f(x, y-step))/(2*step)
	wrapper, zv, dxv, dyv, zp, dxp, dyp = generater.fromFunction(f, dfdx, dfdy, start, end, kernels.kernels, noiseFunctions=noiseFunctions, mask=mask, verbose=verbose)
	solved = m.solve(wrapper, dxv, dyv, kernels.xkernels, kernels.ykernels, verbose=verbose)
	if verbose: print("Comparing...")
	zv = m.normalize(zv, wrapper)
	print("Average difference squared:", compareValues(solved, zv))
	if plotresults:
		if verbose: print("Plotting...")
		plot(zv, wrapper.mask, title="Real values", file="real.html")
		plot(solved, wrapper.mask, "Solved values", file="solved.html")

def sphere(x, y):
	z2 = 12.5**2 - (x-12.5)**2 - (y-12.5)**2
	if z2 <= 0:
		return math.nan
	return math.sqrt(z2)

testFunction(
	#lambda x, y: (
	#	19*(math.cos(x+3)**2)*y
	#	+7*math.pow(y, 1/6)*math.log(x*x)
	#	-15*math.sin(y*y*x-160*math.tan(y))*x
	#),
	#lambda x, y: 5*y*math.log(x),
	sphere,
	#lambda x, y: x**1.35+y**1.25,
	#lambda x, y: x**3-15*(x**2),
	(0, 0),
	(25, 25),
	#dfdx=lambda x, y, z: 3*x*x-30*x,
	#dfdy=lambda x, y, z: 0,
	dfdx=lambda x, y, z: (12.5-x)/z,
	dfdy=lambda x, y, z: (12.5-y)/z,
	#dfdx=lambda x, y, z: 1.35*x**0.35,
	#dfdy=lambda x, y, z: 1.35*y**0.35,
	verbose=True,
	plotresults=True,
)
print("Done.")
