import m
import generater
from kernel import kernel
import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import lsqr
import plotly


plainsize = (256, 256)
plain = np.zeros(plainsize, dtype=np.float_)
gplainx = np.zeros(plainsize, dtype=np.float_)
gplainy = np.zeros(plainsize, dtype=np.float_)
print("Generating sphere...")
mask, hv, gvx, gvy = generater.generateSphereStuff(plain, gplainx, gplainy, 99.9, 128, 128)




print("Generating kernels...")
xkernels = [
	#kernel([
	#	[-0.125, 0, 0.125],
	#	[-0.25, 0, 0.25],
	#	[-0.125, 0, 0.125],
	#]),
	kernel([
		[0, 0, 0],
		[-0.5, 0, 0.5],
		[0, 0, 0],
	]),
	kernel([
		[0, 0, 0],
		[0, -1, 1],
		[0, 0, 0],
	]), kernel([
		[0, 0, 0],
		[-1, 1, 0],
		[0, 0, 0],
	])
]
ykernels = [
	#kernel([
	#	[-0.125, -0.25, -0.125],
	#	[0, 0, 0],
	#	[0.125, 0.25, 0.125],
	#]),
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
print("Generating mask wrapper...")
wrapper = m.maskwrapper(mask, createMap=True, kernels=kernels)



print("Generating Dx matrix...")
Dx = m.applyKernels(wrapper, xkernels)
print("Generating Dy matrix...")
Dy = m.applyKernels(wrapper, ykernels)


print("Generating 1 matrix...")
v1 = sparse.coo_matrix(np.full(wrapper.count(), 1, dtype=np.float_))
print("Generating [Dx Dy 1] matrix...")
A = sparse.vstack([Dx.matrix, Dy.matrix, v1], format="coo")
#temp = np.zeros(wrapper.count())
#temp[0] = 1
#A = sparse.vstack([Dx.matrix, Dy.matrix, temp], format="coo")
print("Generating [Gradx Grady 0] matrix...")
B = np.concatenate((gvx, gvy, np.zeros((1, 1))))
#B = np.concatenate((gvx, gvy))
print("Solving...")
heights = lsqr(A, B)[0]


print("Norming real heights...")
normrealheights = lsqr(
	sparse.vstack([sparse.identity(wrapper.count()), v1]),
	np.concatenate((hv, np.zeros((1, 1)))),
)[0]



print("Comparing...")


t = 0
for i in range(len(normrealheights)):
	t += normrealheights[i]
print(t/wrapper.count())


t = 0
for i in range(len(heights)):
	t += heights[i]
print(t/wrapper.count())


t = 0
for i in range(wrapper.count()):
	t += (normrealheights[i] - heights[i])**2
print(t/wrapper.count())

#print(heights)
#print(hv)
#print(normrealheights)

test = A.dot(normrealheights)
t = 0
for i in range(wrapper.count()):
	#print(test[i], B[i][0], test[i]-B[i][0])
	t += (test[i] - B[i][0])**2
print(t/wrapper.count())

def toMap(mask, heights):
	out = np.full((mask.width(), mask.height()), np.NaN, dtype=np.float_)
	c =  0
	for x in range(mask.width()):
		for y in range(mask.height()):
			if mask.get(x, y):
				out[x][y] = heights[c]
				c += 1
	return out

data = [plotly.graph_objs.Surface(z=toMap(mask, heights))]
layout = plotly.graph_objs.Layout(title="Depth Map")
fig = plotly.graph_objs.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename="output.html")
