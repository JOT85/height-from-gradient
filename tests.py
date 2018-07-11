import testrunner
import math
import testkernels as kernels

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

def testSphere(r, noiseFunctions=(None, None), verbose=False, plot=False):
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
		verbose=verbose,
		plotresults=plot,
	)
	
def testLinear(gx, gy, size, noiseFunctions=(None, None), verbose=False, plot=False):
	return testrunner.testFunction(
		lambda x, y: gx*x+gy*y,
		(0, 0),
		size,
		kernels.kernels,
		kernels.xkernels,
		kernels.ykernels,
		dfdx=lambda x, y, z: gx,
		dfdy=lambda x, y, z: gy,
		verbose=verbose,
		plotresults=plot,
	)
	
print(testLinear(
	2, 2, (12, 12),
	plot=True
))
print(testSphere(
	6,
	plot=True
))
