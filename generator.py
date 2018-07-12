import numpy as np
import math
from arraymask import mask as arraymask
import m

def toVector(p, mask, n=-1):
	"""
	toVector returns an np array, containing only the values from the 2D array (p) that are within the mask.
	it fills the vector in the order:
	(0, 0), (0, 1), (0, 2) ... (1, 0), (1, 1) ...
	Args:
		n, if >= 0, rather than counting the items in the mask, it is assumed that there are n items.
	"""
	#Count values in mask if required
	if n < 0:
		n = 0
		for x in range(mask.width()):
			for y in range(mask.height()):
				if mask.get(x, y):
					n += 1
	#Create an array of length n
	vec = np.zeros(n, dtype=np.float_)
	n = 0
	#For each value within the mask, set the current vector index to it and increment the counter
	for x in range(mask.width()):
		for y in range(mask.height()):
			if mask.get(x, y):
				vec[n] = p[x][y]
				n += 1
	return vec

def fromFunction(f, dfdx, dfdy, start, end, kernels, noiseFunctions=(None, None), mask=None, verbose=False):
	"""
	Creates a height and gradient planes for the given function, along with their corresponding vecotors (from toVector)
	The plains will be the size of end-start, and the x and y coordinates given to the function will range from start to end, so the function will effect be working on that rectangle.
	Unless otherwise specified (see the mask parameter), the kernels argument will be passed to wrapper.removeIsolationsFromKernels
	Args:
		f: Function that maps x and y to z
		dfdx: Returns the gradient with respect to x of the function. It is passed the x, y, and z values.
		dfdx: Returns the gradient with respect to y of the function. It is passed the x, y, and z values.
		noiseFunctions: Tuple of 2 functions or None. If not none, the value of this function will be added to the value of the gradient functions. They recieve the arguments x, y, z, d (where d is the current dx or dy value)
		mask: If not None, this mask will be used instead of creating a new mask.
	"""
	if verbose: print("Carving out plains...")
	#Create the plains
	zplain = np.ndarray((
		end[0] - start[0],
		end[1] - start[1],
	), dtype=np.float_)
	dxplain = np.ndarray((
		end[0] - start[0],
		end[1] - start[1],
	), dtype=np.float_)
	dyplain = np.ndarray((
		end[0] - start[0],
		end[1] - start[1],
	), dtype=np.float_)
	#Create a new mask if there is none given, and note that we don't need to check the mask when we are creating the plains.
	if mask == None:
		if verbose: print("Creating mask...")
		mask = arraymask(
			end[0] - start[0],
			end[1] - start[1],
		)
		checkMask = False
	else:
		checkMask = True
	if verbose: print("Generating plains...")
	#For every item in the mask
	for x in range(start[0], end[0]):
		for y in range(start[1], end[1]):
			if (not checkMask) or mask.get(x, y):
				#Calculate the valiues of the plains
				z = f(x, y)
				dx = dfdx(x, y, z)
				if noiseFunctions[0] is not None:
					dx += noiseFunctions[0](x, y, z, dx)
				dy = dfdy(x, y, z)
				if noiseFunctions[1] is not None:
					dy += noiseFunctions[1](x, y, z, dy)
				#And set them if they are all finite, otherwise, exclude these coordinates from the map
				if math.isfinite(z) and math.isfinite(dx) and math.isfinite(dy):
					zplain[x-start[0]][y-start[1]] = z
					dxplain[x-start[0]][y-start[1]] = dx
					dyplain[x-start[0]][y-start[1]] = dy
				else:
					mask.set(x-start[0], y-start[1], False)
	if verbose: print("Generating mask wrapper...")
	wrapper = m.maskwrapper(mask, createMap=True, kernels=kernels)
	if verbose: print("Creating vectors...")
	return (
		wrapper,
		toVector(zplain, mask, wrapper.count()),
		toVector(dxplain, mask, wrapper.count()),
		toVector(dyplain, mask, wrapper.count()),
		zplain,
		dxplain,
		dyplain,
	)




def generateSphereStuff(p, gpx, gpy, r, cx, cy):
	count = 0
	count = 0
	r2 = r*r
	for x in range(len(p)):
		for y in range(len(p[x])):
			#(x-cx)^2+(y-cy)^2+z^2=r^2
			z2 = r2 - (x-cx)**2 - (y-cy)**2
			#Only carry on if z2 is greater than 0
			if z2 > 0:
				z = math.sqrt(z2)
				p[x][y] = z
				gpx[x][y] = (cx-x)/z
				gpy[x][y] = (cy-y)/z
				count += 1
			elif z2 == 0:
				raise RuntimeError("Don't make the radius and centers integers!!!!!!!!")
	mask = circularmask(len(p), len(p[x]), r, cx, cy)
	heightVector = toVector(p, mask, n=count)
	gradVectorX = toVector(gpx, mask, n=count)
	gradVectorY = toVector(gpy, mask, n=count)
	return (mask, heightVector, gradVectorX, gradVectorY)

class circularmask:
	def __init__(self, w, h, r, cx, cy):
		self.w = w
		self.h = h
		self.r2 = r*r
		self.cx = cx
		self.cy = cy
	def width(self):
		return self.w
	def height(self):
		return self.h
	def get(self, x, y):
		return (self.r2 - (x-self.cx)**2 - (y-self.cy)**2) >= 0
	def set(self, x, y, v):
		raise RuntimeError("The circlular mask is good!!! Go away!")
