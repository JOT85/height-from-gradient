class kernel:
	"""represents a kernel"""
	def __init__(self, data):
		"""takes a square 2D list/array/whatever you like that is indexable, and wrapps it in a nice interface"""
		self.kernel = data
	def size(self):
		return len(self.kernel)
	def get(self, x, y):
		return self.kernel[y][x]
