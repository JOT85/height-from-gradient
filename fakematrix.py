class matrix:
	def __init__(self, w, h):
		self.w = w
		self.h = h
	def set(self, x, y, v):
		if x < 0 or y < 0 or x >= self.w or y >= self.h:
			raise RuntimeError("Out of matrix bounds")
		print("Marix ({},{}) = {}".format(x, y, v))
