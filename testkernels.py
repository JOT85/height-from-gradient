from kernel import kernel
from kernel import normalizex, normalizey

xkernels = [
	#kernel(normalizex([
	#	[0, -1, 0, 1, 0],
	#	[-1, -2, 0, 2, 1],
	#	[-2, -5, 0, 5, 2],
	#	[-1, -2, 0, 2, 1],
	#	[0, -1, 0, 1, 0],
	#])),
	kernel(([
		[-1/12, 0, 1/12],
		[-1/3, 0, 1/3],
		[-1/12, 0, 1/12],
	])),
	kernel([
		[0, 0, 0],
		[-0.5, 0, 0.5],
		[0, 0, 0],
	]),
	kernel([
		[0, 0, 0],
		[0, -1, 1],
		[0, 0, 0],
	]),
	kernel([
		[0, 0, 0],
		[-1, 1, 0],
		[0, 0, 0],
	])
]
ykernels = [
	#kernel(normalizey([
	#	[0,  -1, -2, -1, 0],
	#	[-1, -2, -5, -2, -1],
	#	[0,   0,  0,  0, 0],
	#	[1,   2,  5,  2, 1],
	#	[0,   1,  2,  1, 0],
	#])),
	kernel([
		[-1/12, -1/3, -1/12],
		[0, 0, 0],
		[1/12, 1/3, 1/12],
	]),
	kernel([
		[0, -0.5, 0],
		[0, 0, 0],
		[0, 0.5, 0],
	]),
	kernel([
		[0, 0, 0],
		[0, -1, 0],
		[0, 1, 0],
	]), kernel([
		[0, -1, 0],
		[0, 1, 0],
		[0, 0, 0],
	])
]

kernels = []
kernels.extend(ykernels)
kernels.extend(xkernels)
