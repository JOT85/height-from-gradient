import testrunner
import math
import testkernels as kernels
import random
import generator
import m
import scipy.io
import numpy as np
from plotheights import plot

class sphere:
	def __init__(self, r, cx, cy):
		self.cx = cx
		self.cy = cy
		self.r2 = r*r
	def z(self, x, y):
		z2 = self.r2 - (x-self.cx)**2 - (y-self.cy)**2
		if z2 < 0:
			return math.nan
		return math.sqrt(z2)
	def dzdx(self, x, y, z):
		if z == 0:
			return math.nan
		return (self.cx-x)/z
	def dzdy(self, x, y, z):
		if z == 0:
			return math.nan
		return (self.cy-y)/z

def testSphere(r, noiseFunctions=(None, None), verbose=False, plot=False, plotfileprefix=""):
	s = sphere(r, r, r)
	return testrunner.testFunction(
		s.z,
		(0, 0),
		(r*2, r*2),
		kernels.kernels,
		kernels.xkernels,
		kernels.ykernels,
		dfdx=s.dzdx,
		dfdy=s.dzdy,
		noiseFunctions=noiseFunctions,
		verbose=verbose,
		plotresults=plot,
		plotfileprefix=plotfileprefix,
	)
	
def testLinear(gx, gy, size, noiseFunctions=(None, None), verbose=False, plot=False, plotfileprefix=""):
	return testrunner.testFunction(
		lambda x, y: gx*x+gy*y,
		(0, 0),
		size,
		kernels.kernels,
		kernels.xkernels,
		kernels.ykernels,
		dfdx=lambda x, y, z: gx,
		dfdy=lambda x, y, z: gy,
		noiseFunctions=noiseFunctions,
		verbose=verbose,
		plotresults=plot,
		plotfileprefix=plotfileprefix,
	)
	
def randomNoise(x, y, z, d):
	return (random.random()-0.5)*d
	
#print(testLinear(
#	2, 2, (12, 12),
#	plot=True, plotfileprefix="linear.",
#	#noiseFunctions=(randomNoise, randomNoise),
#))
#print(testSphere(
#	60,
#	plot=True, plotfileprefix="sphere.",
#	#noiseFunctions=(randomNoise, randomNoise),
#))

plotfileprefix="hi."
d = scipy.io.loadmat("/home/jp/Downloads/teapot_disparity.mat")
#tu_mask = generator.arraymask(len(d["depthmap"]), len(d["depthmap"][1]))
#plot(depths, tu_mask, title="Real values", file=plotfileprefix+"real.html")
#exit()

wrapper = generator.generateMaskWrapper(d["depthmap"], kernels.kernels1)
depths = generator.toVector(d["depthmap"], wrapper.mask)
grad = m.solveGrad(wrapper, depths, kernels.xkernels1, kernels.ykernels1, verbose=True)
solved = m.normalize(m.solve(wrapper, grad[:len(grad)//2], grad[len(grad)//2:], kernels.xkernels2, kernels.ykernels2, verbose=True), wrapper)

print("Comparison:", testrunner.compareValues(depths, solved, wrapper))

plot(m.normalize(depths, wrapper), wrapper.mask, title="Real values", file=plotfileprefix+"real.html")
plot(solved, wrapper.mask, "Solved values", file=plotfileprefix+"solved.html")

exit()

SIZE = 20

print(testrunner.testFunction(
	#lambda x, y: 1e-2*(x**2+x/y**2-5+math.log(y, x)),
	#lambda x, y: 5e-2*(-2*(x-25)**2+(y-25)**2),
	lambda x, y: (x/(SIZE/1.4) - (1.4/1.8969))**4 - (y/(SIZE/2.2) - 2.2/2)**2 + 1.269,
	#lambda x, y: (x/(SIZE/2))**2 + (y/(SIZE/1.2))**2,
	(0, 0),
	(SIZE+1, SIZE+1),
	kernels.kernels,
	kernels.xkernels,
	kernels.ykernels,
	#dfdx=lambda x, y, z: 1e-2*(2*x+1/y**2-math.log(y, x)/(x*math.log(x))),
	#dfdx=lambda x, y, z: 5-x/5,
	#dfdx=lambda x, y, z: 5-x/5,
	dfdx=lambda x, y, z: 4 * (1.4/SIZE) * (x/(SIZE/1.4) - (1.4/1.8969))**3,
	#dfdx=lambda x, y, z: 2*x/(SIZE/2)**2,
	#dfdy=lambda x, y, z: 1e-2*(-2*x*y**(-3)+1/(y*math.log(x))),
	#dfdy=lambda x, y, z: y/10-5/2,
	dfdy=lambda x, y, z: -(2/(SIZE/2.2))*(y/(SIZE/2.2) - 2.2/2),
	#dfdy=lambda x, y, z: 2*y/(SIZE/1.2)**2,
	verbose=True,
	plotresults=True,
))
