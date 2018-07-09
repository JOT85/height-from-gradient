import numpy as np

class mask:
	def __init__(self, w, h, default=True):
		self.w = w
		self.h = h
		self.array = np.full((w, h), default, dtype=np.bool_)
	def width(self):
		return self.w
	def height(self):
		return self.h
	def get(self, x, y):
		if x < 0 or y < 0 or x >= self.w or y >= self.h:
			return False
		return self.array[x][y]
	def set(self, x, y, v):
		self.array[x][y] = v

