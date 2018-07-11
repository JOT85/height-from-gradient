from kernel import kernel

xkernels = [
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
kernels.extend(ykernels[::-1])
kernels.extend(xkernels[::-1])
