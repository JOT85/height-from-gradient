import numpy as np
from scipy.sparse import lil_matrix as matrixtype

class matrix:
	def __init__(self, w, h):
		self.w = w
		self.h = h
		self.matrix = matrixtype((h, w), dtype=np.float_)
	def set(self, x, y, v):
		self.matrix[y, x] = v
	def resize(self, w, h):
		self.w = w
		self.h = h
		self.matrix.resize((h, w))
	def width(self):
		return self.w
	def height(self):
		return self.h
