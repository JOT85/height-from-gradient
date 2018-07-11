def checkGenerator():
	m1, z1, dx1, dy1 = generator.generateSphereStuff(
		np.ndarray((256, 256)),
		np.ndarray((256, 256)),
		np.ndarray((256, 256)),
		59.9,
		100,
		100,
	)

	r2 = 59.9**2
	def f(x, y):
		z2 = r2 - (x-100)**2 - (y-100)**2
		if z2 < 0:
			return math.nan
		return math.sqrt(z2)

	m2, z2, dx2, dy2, _, _ , _ = generator.fromFunction(
		f,
		lambda x, y, z: (100-x)/z,
		lambda x, y, z: (100-y)/z,
		(0, 0),
		(256, 256),
	)

	if m1.width() != m2.width() or m1.height() != m2.height():
		raise RuntimeError("Mask dimensions not consistant")
	for x in range(m1.width()):
		for y in range(m1.height()):
			if m1.get(x, y) != m2.get(x, y):
				raise RuntimeError("Masks not equal")

	def checkEqual(a, b, label):
		if len(a) != len(b):
			raise RuntimeError(label + " dimensions not consistant")
		for i in range(len(a)):
			if a[i][0] != b[i][0]:
				raise RuntimeError(label + " not equal")

	checkEqual(z1, z2, "z")
	checkEqual(dx1, dx2, "dx")
	checkEqual(dy1, dy2, "dy")

	print("All good!!!")