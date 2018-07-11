import generator
import numpy as np
import math
import m
import testkernels as kernels
from plotheights import plot

def compareValues(a, b):
	"""Returns the average squared difference of all the values in the arrays a and b"""
	if len(a) != len(b):
		raise RuntimeError("vectors must be the same size to compare")
	t = 0
	for i in range(len(a)):
		t += (a[i]-b[i])**2
	return t / len(a)

def testFunction(f, start, end, kernels, xkernels, ykernels, dfdx=None, dfdy=None, noiseFunctions=(None, None), mask=None, step = 0.01, verbose=False, plotresults=False):
	"""
	Solves for the height (from the gradients) using the given kernels and compares the solved heights to the real heights.
	
	Args:
		f: The function that maps x and y to z
		start: The top left of the rectangle to be tested
		end: The bottom right of the rectangle to be tested
		kernels: A list of all the kernels that should be tested when removing isolations
		xkernels: The kernels to use when calculating the x gradient
		ykernels: The kernels to use when calculating the y gradient
		dfdx: Should return the derivative with respect to x of f. If None, a partial derivative of f with step step will be used.
		dfdy: Should return the derivative with respect to y of f. If None, a partial derivative of f with step step will be used.
		noiseFunctions: noiseFunctions passed to generator.fromFunction
		mask: If not none, this mask will be used, otherwise, all finite heights will be used.
		step: The step to use when finding partial derivatives of f (only if dfdx or dfdy are None)
		plotResults: If True, plotly will be used to plot the real and solved height values.
		
	Returns:
		The average square difference between the solved and real height values.
	"""
	if verbose: print("Testing...")
	if dfdx == None:
		dfdx = lambda x, y, z: (f(x+step, y) - f(x-step, y))/(2*step)
	if dfdy == None:
		dfdy = lambda x, y, z: (f(x, y+step) - f(x, y-step))/(2*step)
	wrapper, zv, dxv, dyv, _, _, _ = generator.fromFunction(f, dfdx, dfdy, start, end, kernels, noiseFunctions=noiseFunctions, mask=mask, verbose=verbose)
	solved = m.solve(wrapper, dxv, dyv, xkernels, ykernels, verbose=verbose)
	if verbose: print("Comparing...")
	zv = m.normalize(zv, wrapper)
	if plotresults:
		if verbose: print("Plotting...")
		plot(zv, wrapper.mask, title="Real values", file="real.html")
		plot(solved, wrapper.mask, "Solved values", file="solved.html")
	return compareValues(solved, zv)

