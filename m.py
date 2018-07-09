from sparsematrix import matrix
from fakemask import mask
from kernel import kernel

class maskwrapper:
	"""Wraps mask to provide utilities"""
	def __init__(self, mask, kernels=[], removeIsolationsSpeedy=False, createMap=False):
		self.mask = mask
		if removeIsolationsSpeedy:
			self.removeIsolations()
		elif len(kernels) != 0:
			self.removeIsolationsFromKernels(kernels)
		if createMap:
			self.createMap()
		else:
			self.map = {}
			self.c = 0
			self.evens = []
			self.odds = []
	def createMap(self):
		"""createMap resets and fills the map, linking each mask coordinate to its index in the sliced column vector"""
		#Reset everything
		self.map = {}
		self.c = 0
		#For each pixel that is within the map
		for x in range(self.mask.width()):
			for y in range(self.mask.height()):
				if self.mask.get(x, y):
					#If the map for the x coordinate already exists, add the y coordinate to it,
					# otherwise, create the dectionary.
					if x in self.map:
						self.map[x][y] = self.c
					else:
						self.map[x] = {y: self.c}
					self.c += 1
	def get(self, x, y):
		"""get the index of the given coordinate"""
		return self.map[x][y]
	def count(self):
		"""Returns the total amount of pixels contained by the mask when the map was last created"""
		return self.c
	def isDataThere(self, x, y, k):
		"""Determines if a kernel k can be applied to the mask for the point (x, y)"""
		radius = int((k.size()-1)/2)
		#For every data point in the kernel that is not 0 (so is required)
		for kx in range(k.size()):
			for ky in range(k.size()):
				if k.get(kx, ky) != 0:
					#If the mask does not include that pixel,
					# then this kernel cannot be applied. So return False.
					if not self.mask.get(x-radius+kx, y-radius+ky):
						return False
		return True
	def removeIsolations(self):
		"""Removes pixels from a mask that have no direct naibours"""
		changed = False
		#consec keeps track of the value of the last y coordinate,
		# so that it doesn't have to be looked up immediatally afterwards.
		consec = False
		for x in range(self.mask.width()):
			y = 0
			while y < self.mask.height():
				if self.mask.get(x, y):
					#If there is no last y and no next y, remove it.
					if (not consec) and (not self.mask.get(x, y+1)):
						self.mask.set(x, y, False)
						consec = False
						changed = True
						#We can skip a pixel, because we know the next one isn't in the map.
						y += 1
					#And the same with x, but only if we haven't removed it
					elif (not self.mask.get(x-1, y)) and (not self.mask.get(x+1, y)):
						self.mask.set(x, y, False)
						changed = True
						consec = False
					else:
						#YAY!!! This pixel is all good!
						consec = True
				else:
					consec = False
				y += 1
		#If we have modified the mask, then we need to check again, because we might have
		# removed points used by other kernels after we checked that kernel.
		#This will keep going until nothing needs changing so gradients can be calculated for all pixels.
		if changed:
			self.removeIsolations()
	def removeIsolationsFromKernels(self, kernels):
		"""Removes pixels from a mask whomes gradiant cannot be determined from and of the given kernels.
		They are checked in the order of which they are in the list. So the most likely to fit kernel should be first.
		Not the highest priority."""
		changed = False
		for x in range(self.mask.width()):
			for y in range(self.mask.height()):
				if self.mask.get(x, y):
					#For each pixel, assume its isolated, if its gradiant can be detemrined, then we know we aren't isolated.
					isolated = True
					for k in kernels:
						if self.isDataThere(x, y, k):
							isolated = False
							break
					if isolated:
						changed = True
						self.mask.set(x, y, False)
		#If we have modified the mask, then we need to check again, because we might have
		# removed points used by other kernels after we checked that kernel.
		#This will keep going until nothing needs changing so gradients can be calculated for all pixels.
		if changed:
			self.removeIsolationsFromKernels(kernels)

def isEdge(wrapper, x, y):
	return False
	return (
		(not wrapper.mask.get(x-1, y))
		or (not wrapper.mask.get(x-1, y-1))
		or (not wrapper.mask.get(x, y-1))
		or (not wrapper.mask.get(x+1, y))
		or (not wrapper.mask.get(x+1, y+1))
		or (not wrapper.mask.get(x, y+1))
		or (not wrapper.mask.get(x-2, y))
		or (not wrapper.mask.get(x-2, y-1))
		or (not wrapper.mask.get(x-2, y-2))
		or (not wrapper.mask.get(x-1, y-2))
		or (not wrapper.mask.get(x, y-2))
		or (not wrapper.mask.get(x+2, y))
		or (not wrapper.mask.get(x+2, y+1))
		or (not wrapper.mask.get(x+2, y+2))
		or (not wrapper.mask.get(x+1, y+2))
		or (not wrapper.mask.get(x, y+2))
	)

def applyKernels(data, kernels):
	#Create the output matrix
	m = matrix(data.count(), data.count())
	#c represents the nth pixel that we are applying the transform to
	c = 0
	#For all pixels within the map
	for x in range(data.mask.width()):
		for y in range(data.mask.height()):
			if data.mask.get(x, y):
				#Find the first kernel we can use kernel we can use
				for k in kernels:
					if data.isDataThere(x, y, k):
						#And iterate through the pixels in the kernel, and add them to the matrix
						# if they aren't 0.
						radius = int((k.size()-1)/2)
						for kx in range(k.size()):
							for ky in range(k.size()):
								if k.get(kx, ky) != 0:
									m.set(data.get(x-radius+kx, y-radius+ky), c, k.get(kx, ky))
						c += 1
						break
	return m

def createHeightNormMatrix(data):
	norm = matrix(data.count(), 1)
	others = matrix(data.count(), data.count())
	othersY = 0
	for x in range(data.mask.width()):
		for y in range(data.mask.height()):
			if data.mask.get(x, y) and not isEdge(data, x, y):
				#xeven = x % 2 == 0
				#yeven = y % 2 == 0
				#if (yeven and xeven) or (not yeven and not xeven):
				if y % 2 == x % 2:
					norm.set(data.get(x, y), 0, 1)
				elif data.mask.get(x-1, y) and data.mask.get(x+1, y) and data.mask.get(x, y-1) and data.mask.get(x, y+1):
					others.set(data.get(x+1, y), othersY, 1)
					others.set(data.get(x-1, y), othersY, 1)
					others.set(data.get(x, y+1), othersY, 1)
					others.set(data.get(x, y-1), othersY, 1)
					others.set(data.get(x, y), othersY, -4)
					othersY += 1
	others.resize(data.count(), othersY)
	return (norm, others)


import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import lsqr

def solve(wrapper, gx, gy, xkernels, ykernels, verbose=False):
	if verbose: print("Generating Dx matrix...")
	Dx = applyKernels(wrapper, xkernels)
	if verbose: print("Generating Dy matrix...")
	Dy = applyKernels(wrapper, ykernels)
	if verbose: print("Generating normalization matrix...")
	norm, others = createHeightNormMatrix(wrapper)
	if verbose: print("Generating A and b matricies...")
	#v1 = sparse.coo_matrix(np.full(wrapper.count(), 1, dtype=np.float_))
	## A = [ Dx Dy 1k ]
	# A = [ Dx Dy norm others ]
	A = sparse.vstack([Dx.matrix, Dy.matrix, norm.matrix, others.matrix], format="coo")
	print(norm.matrix.toarray())
	for fu in others.matrix.toarray():
		print(fu)
	# b = [ Gx Gy 0n ]
	#b = np.concatenate((gx, gy, np.zeros((1, 1))))
	b = np.concatenate((gx, gy, np.zeros(1+others.height())))
	# Solve Az=b
	if verbose: print("Solving...")
	return lsqr(A, b)[0]

def normalize(v, wrapper):
	return v - np.mean(v)
