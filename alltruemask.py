class mask:
	def __init__(self, w, h):
		self.w = w
		self.h = h
	def width(self):
		return self.w
	def height(self):
		return self.h
	def get(self, x, y):
		if x == 0 and y == 0:
			return False
		if x < 0 or y < 0 or x >= self.w or y >= self.h:
			return False
		return True
	def set(self, x, y, v):
		print("Mask set ({},{}) to {}".format(x, y, v))
