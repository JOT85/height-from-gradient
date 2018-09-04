from kernel import kernel
import savitzky_golay_filter as sgf

xkernels1 = [
	kernel(sgf.makeIt(71, 5, 12, 12, 1, 0)),
	kernel(sgf.makeIt(25, 5, 12, 12, 1, 0)),
	kernel(sgf.makeIt(21, 3, 10, 10, 1, 0)),
	kernel(sgf.makeIt(9, 3, 4, 4, 1, 0)),
	kernel(sgf.makeIt(5, 3, 2, 2, 1, 0)),
	kernel(sgf.makeIt(3, 2, 1, 1, 1, 0)),
	kernel(sgf.makeIt(3, 2, 0, 1, 1, 0)),
	kernel(sgf.makeIt(3, 2, 1, 0, 1, 0)),
	kernel(sgf.makeIt(3, 2, 2, 1, 1, 0)),
	kernel(sgf.makeIt(3, 2, 1, 2, 1, 0)),
	kernel(sgf.makeIt(3, 2, 0, 0, 1, 0)),
	kernel(sgf.makeIt(3, 2, 0, 2, 1, 0)),
	kernel(sgf.makeIt(3, 2, 2, 0, 1, 0)),
	kernel(sgf.makeIt(3, 2, 2, 2, 1, 0)),
]

ykernels1 = [
	kernel(sgf.makeIt(71, 5, 12, 12, 0, 1)),
	kernel(sgf.makeIt(25, 5, 12, 12, 0, 1)),
	kernel(sgf.makeIt(21, 3, 10, 10, 0, 1)),
	kernel(sgf.makeIt(9, 3, 4, 4, 0, 1)),
	kernel(sgf.makeIt(5, 3, 2, 2, 0, 1)),
	kernel(sgf.makeIt(3, 2, 1, 1, 0, 1)),
	kernel(sgf.makeIt(3, 2, 0, 1, 0, 1)),
	kernel(sgf.makeIt(3, 2, 1, 0, 0, 1)),
	kernel(sgf.makeIt(3, 2, 2, 1, 0, 1)),
	kernel(sgf.makeIt(3, 2, 1, 2, 0, 1)),
	kernel(sgf.makeIt(3, 2, 0, 0, 0, 1)),
	kernel(sgf.makeIt(3, 2, 0, 2, 0, 1)),
	kernel(sgf.makeIt(3, 2, 2, 0, 0, 1)),
	kernel(sgf.makeIt(3, 2, 2, 2, 0, 1)),
]

xkernels2 = [
	kernel(sgf.makeIt(13, 3, 4, 4, 1, 0)),
	kernel(sgf.makeIt(9, 3, 4, 4, 1, 0)),
	kernel(sgf.makeIt(5, 3, 2, 2, 1, 0)),
	kernel(sgf.makeIt(3, 2, 1, 1, 1, 0)),
	kernel(sgf.makeIt(3, 2, 0, 1, 1, 0)),
	kernel(sgf.makeIt(3, 2, 1, 0, 1, 0)),
	kernel(sgf.makeIt(3, 2, 2, 1, 1, 0)),
	kernel(sgf.makeIt(3, 2, 1, 2, 1, 0)),
	kernel(sgf.makeIt(3, 2, 0, 0, 1, 0)),
	kernel(sgf.makeIt(3, 2, 0, 2, 1, 0)),
	kernel(sgf.makeIt(3, 2, 2, 0, 1, 0)),
	kernel(sgf.makeIt(3, 2, 2, 2, 1, 0)),
]

ykernels2 = [
	kernel(sgf.makeIt(13, 3, 4, 4, 0, 1)),
	kernel(sgf.makeIt(9, 3, 4, 4, 0, 1)),
	kernel(sgf.makeIt(5, 3, 2, 2, 0, 1)),
	kernel(sgf.makeIt(3, 2, 1, 1, 0, 1)),
	kernel(sgf.makeIt(3, 2, 0, 1, 0, 1)),
	kernel(sgf.makeIt(3, 2, 1, 0, 0, 1)),
	kernel(sgf.makeIt(3, 2, 2, 1, 0, 1)),
	kernel(sgf.makeIt(3, 2, 1, 2, 0, 1)),
	kernel(sgf.makeIt(3, 2, 0, 0, 0, 1)),
	kernel(sgf.makeIt(3, 2, 0, 2, 0, 1)),
	kernel(sgf.makeIt(3, 2, 2, 0, 0, 1)),
	kernel(sgf.makeIt(3, 2, 2, 2, 0, 1)),
]

def mix(k1, k2):
	out = []
	for i in range(len(k1)-1, -1, -1):
		out.append(k1[i])
		out.append(k2[i])
	return out

kernels1 = mix(xkernels1, ykernels1)
kernels2 = mix(xkernels2, ykernels2)

xkernels = [
	#kernel(([
	#	[-1/12, 0, 1/12],
	#	[-1/3, 0, 1/3],
	#	[-1/12, 0, 1/12],
	#])),
	#kernel(sgf.makeXGradientKernel(11, 4)),
	#kernel(sgf.makeXGradientKernel(7, 3)),
	#kernel(sgf.makeXGradientKernel(5, 3)),
	#kernel(sgf.makeXGradientKernel(5, 3)),
	#kernel(sgf.makeXGradientKernel(3, 2)),
	kernel(sgf.makeIt(11, 4, 5, 5, 1, 0)),
	kernel(sgf.makeIt(5, 3, 2, 2, 1, 0)),
	kernel(sgf.makeIt(3, 2, 1, 1, 1, 0)),
	kernel(sgf.makeIt(3, 2, 0, 1, 1, 0)),
	kernel(sgf.makeIt(3, 2, 1, 0, 1, 0)),
	kernel(sgf.makeIt(3, 2, 2, 1, 1, 0)),
	kernel(sgf.makeIt(3, 2, 1, 2, 1, 0)),
	kernel(sgf.makeIt(3, 2, 0, 0, 1, 0)),
	kernel(sgf.makeIt(3, 2, 0, 2, 1, 0)),
	kernel(sgf.makeIt(3, 2, 2, 0, 1, 0)),
	kernel(sgf.makeIt(3, 2, 2, 2, 1, 0)),
	#kernel(sgf.makeXGradientKernelEdgeAbove(5, 3)),
	#kernel(sgf.makeXGradientKernelEdgeBelow(5, 3)),
	#kernel(sgf.makeXGradientKernelEdgeAbove(3, 2)),
	#kernel(sgf.makeXGradientKernelEdgeBelow(3, 2)),
	#kernel(sgf.makeXGradientKernel(3, 1)),
	#kernel([
	#	[0, 0, 0],
	#	[-0.5, 0, 0.5],
	#	[0, 0, 0],
	#]),
	#kernel([
	#	[0, 0, 0],
	#	[-1, 1, 0],
	#	[0, 0, 0],
	#]),
	#kernel([
	#	[0, 0, 0],
	#	[0, -1, 1],
	#	[0, 0, 0],
	#]),
]
ykernels = [
	kernel(sgf.makeIt(11, 4, 5, 5, 0, 1)),
	kernel(sgf.makeIt(5, 3, 2, 2, 0, 1)),
	kernel(sgf.makeIt(3, 2, 1, 1, 0, 1)),
	kernel(sgf.makeIt(3, 2, 0, 1, 0, 1)),
	kernel(sgf.makeIt(3, 2, 1, 0, 0, 1)),
	kernel(sgf.makeIt(3, 2, 2, 1, 0, 1)),
	kernel(sgf.makeIt(3, 2, 1, 2, 0, 1)),
	kernel(sgf.makeIt(3, 2, 0, 0, 0, 1)),
	kernel(sgf.makeIt(3, 2, 0, 2, 0, 1)),
	kernel(sgf.makeIt(3, 2, 2, 0, 0, 1)),
	kernel(sgf.makeIt(3, 2, 2, 2, 0, 1)),
	#kernel([
	#	[-1/12, -1/3, -1/12],
	#	[0, 0, 0],
	#	[1/12, 1/3, 1/12],
	#]),
	#kernel(sgf.makeYGradientKernel(11, 4)),
	#kernel(sgf.makeYGradientKernel(7, 3)),
	#kernel(sgf.makeYGradientKernel(5, 3)),
	#kernel(sgf.makeYGradientKernel(3, 2)),
	#kernel(sgf.makeYGradientKernelEdgeLeft(3, 2)),
	#kernel(sgf.makeYGradientKernelEdgeRight(3, 2)),
	#kernel(sgf.makeYGradientKernel(3, 1)),
	#kernel([
	#	[0, -0.5, 0],
	#	[0, 0, 0],
	#	[0, 0.5, 0],
	#]),
	#kernel([
	#	[0, -1, 0],
	#	[0, 1, 0],
	#	[0, 0, 0],
	#]),
	#kernel([
	#	[0, 0, 0],
	#	[0, -1, 0],
	#	[0, 1, 0],
	#]),
]

kernels = []
kernels.extend(ykernels[::-1])
kernels.extend(xkernels[::-1])
