from sparsematrix import matrix
from kernel import kernel

import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import lsqr

class maskwrapper:
	"""Wraps mask to provide mapping, counting, matching, utilities"""
	def __init__(self, mask, kernels=[], removeIsolationsSpeedy=False, createMap=False):
		"""
		Args:
			mask The mask to wrap
			kernels: List of kernels that will be used with this mask. If not empty, self.removeIsolationsFromKernels(kernels) is called.
			removeIsolationsSpeedy: If True, self.removeIsolations() will be called. kernels will also be ignored.
			createMap: If true, self.createMap will be called after removing any isolations from the given kernels.
		"""
		self.mask = mask
		#Run the relivent isolation remover
		if removeIsolationsSpeedy:
			self.removeIsolations()
		elif len(kernels) != 0:
			self.removeIsolationsFromKernels(kernels)
		if createMap:
			self.createMap()
		else:
			#We aren't creating a map, so initialize the parameters to nil values.
			self.map = {}
			self.c = 0
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
		"""get the index of the given coordinate (createMap must have been called first)"""
		return self.map[x][y]
	def getReverse(self, n):
		"""getReverse does the opposite of get - so takes an index in the vectorized map, and returns the coordinates of that point.
		It is not designed to be called frequently."""
		n = n % self.count()
		s = 0
		for x in range(self.mask.width()):
			for y in range(self.mask.height()):
				if self.mask.get(x, y):
					if s == n:
						return (x, y)
					s += 1
		return (-1, -1)
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

def applyKernels(data, kernels):
	"""
	Creates a matrix, that will apply the first kernel where all the pixels needed are present within the mask to each pixel within the mask.
	Args:
		data: maskwrapper wrapping the mask that needs to be applied. removeIsolations (FromKernels?) and createMap must have been called before passing it to this function.
		kernels: the list of kernels to apply, in order of priority (index 0 has highest priority).
	"""	
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
	"""
	Creates a martix, which the dot product of should be a column vector full of 0s for the heights to be normalized.
	The first row has a 1 for every other pixel (with the mask layed on top, so not necisarily every other pixel in the final height vector), and thefore, when the product is 0, every other pixel will be averaged to 0.
	The rest of the rows, then apply a a kernel to each pixel (if possible). This kernel averages all of the immediate horisontal and vertical naighbouring pixels, and subtracts the central pixel. Making this 0 would place its height in between its naighbours.
	"""
	out = matrix(data.count(), data.count()+1)
	othersY = 1
	#For every point in the mask
	for x in range(data.mask.width()):
		for y in range(data.mask.height()):
			if data.mask.get(x, y):
				#If both points are even, or both are odd, then it needs to be added the the norm matrix
				if y % 2 == x % 2:
					out.set(data.get(x, y), 0, 1)
				elif data.mask.get(x-1, y) and data.mask.get(x+1, y) and data.mask.get(x, y-1) and data.mask.get(x, y+1):
					out.set(data.get(x+1, y), othersY, 1)
					out.set(data.get(x-1, y), othersY, 1)
					out.set(data.get(x, y+1), othersY, 1)
					out.set(data.get(x, y-1), othersY, 1)
					out.set(data.get(x, y), othersY, -4)
					othersY += 1
	out.resize(data.count(), othersY)
	return out

def solveGrad(wrapper, z, xkernels, ykernels, verbose=False):
	"""Given the mask (wrapped), height values. SolveGrad solves for the gradient map, using the given convolution kernels."""
	if verbose: print("Generating Dx matrix...")
	Dx = applyKernels(wrapper, xkernels)
	if verbose: print("Generating Dy matrix...")
	Dy = applyKernels(wrapper, ykernels)
	if verbose: print("Generating A and b matricies...")
	# A = [ Dx Dy ]
	A = sparse.vstack([Dx.matrix, Dy.matrix], format="coo")
	# b = [ Gx Gy ]
	# Solve Az=b for z
	if verbose: print("Solving...")
	return A.dot(z)

def solve(wrapper, gx, gy, xkernels, ykernels, verbose=False):
	"""Given the mask (wrapped), x gradient values, and y gradient values. Solve solves for the height map, using the given convolution kernels."""
	if verbose: print("Generating Dx matrix...")
	Dx = applyKernels(wrapper, xkernels)
	if verbose: print("Generating Dy matrix...")
	Dy = applyKernels(wrapper, ykernels)
	if verbose: print("Generating normalization matrix...")
	norm = createHeightNormMatrix(wrapper)
	if verbose: print("Generating A and b matricies...")
	# A = [ Dx Dy norm ]
	A = sparse.vstack([Dx.matrix, Dy.matrix, norm.matrix], format="coo")
	# b = [ Gx Gy 0n ]
	b = np.concatenate((gx, gy, np.zeros(norm.height())))
	# Solve Az=b for z
	if verbose: print("Solving...")
	return lsqr(A, b)[0]

def normalize(v, wrapper):
	"""Returns the given vector, however with all the points averaging to 0"""
	return v - np.mean(v)
