import numpy as np
import math
from arraymask import mask as arraymask
import m

def toVector(p, mask, n=-1):
	if n == -1:
		n = 0
		for x in range(mask.width()):
			for y in range(mask.height()):
				if mask.get(x, y):
					n += 1
	#vec = np.zeros((n, 1), dtype=np.float_)
	vec = np.zeros(n, dtype=np.float_)
	n = 0
	for x in range(mask.width()):
		for y in range(mask.height()):
			if mask.get(x, y):
				vec[n] = p[x][y]
				n += 1
	return vec

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

def fromFunction(f, dfdx, dfdy, start, end, kernels, noiseFunctions=(None, None), mask=None, verbose=False):
	if verbose: print("Carving out plains...")
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
	if mask == None:
		if verbose: print("Creating mask...")
		mask = arraymask(
			end[0] - start[0],
			end[1] - start[1],
		)
		c = mask.width()*mask.height()
		checkMask = False
	else:
		if verbose: print("Counting mask...")
		c = 0
		for x in range(mask.width()):
			for y in range(mask.height()):
				if mask.get(x, y):
					c += 1
		checkMask = True
	if verbose: print("Generating plains...")
	for x in range(start[0], end[0]):
		for y in range(start[1], end[1]):
			if (not checkMask) or mask.get(x, y):
				z = f(x, y)
				dx = dfdx(x, y, z)
				if noiseFunctions[0] is not None:
					dx += noiseFunctions(x, y, z)
				dy = dfdy(x, y, z)
				if noiseFunctions[1] is not None:
					dy += noiseFunctions(x, y, z)
				if math.isfinite(z) and math.isfinite(dx) and math.isfinite(dy):
					zplain[x-start[0]][y-start[1]] = z
					dxplain[x-start[0]][y-start[1]] = dx
					dyplain[x-start[0]][y-start[1]] = dy
				else:
					mask.set(x-start[0], y-start[1], False)
					c -= 1
	if verbose: print("Generating mask wrapper...")
	wrapper = m.maskwrapper(mask, createMap=True, kernels=kernels)
	if verbose: print("Creating vectors...")
	return (
		wrapper,
		toVector(zplain, mask, c),
		toVector(dxplain, mask, c),
		toVector(dyplain, mask, c),
		zplain,
		dxplain,
		dyplain,
	)
