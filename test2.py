from scipy.io import loadmat
import scipy.sparse as sparse
from scipy.sparse.linalg import lsqr
import numpy as np
import plotly
import math

import testkernels as kernels
import m

data = loadmat("testdata.mat")

class matmask:
	def __init__(self, data):
		self.data = data
		self.w = len(data)
		self.h = len(data[0])
	def width(self):
		return self.w
	def height(self):
		return self.h
	def get(self, x, y):
		if x < 0 or y < 0 or x >= self.w or y >= self.h:
			return False
		return self.data[x][y] != 0
	def set(self, x, y, v):
		if v:
			self.data[x][y] = 1
		else:
			self.data[x][y] = 0
			
mask = matmask(data["mask"])

print("Generating mask wrapper...")
wrapper = m.maskwrapper(mask, kernels=kernels.kernels, createMap=True)

print("Generating Dx matrix...")
Dx = m.applyKernels(wrapper, kernels.xkernels)
print("Generating Dy matrix...")
Dy = m.applyKernels(wrapper, kernels.ykernels)


print("Generating matrix of 0s...")
v0 = sparse.coo_matrix(np.full(wrapper.count(), 0, dtype=np.float_))
print("Generating matrix of 1s...")
v1 = sparse.coo_matrix(np.full(wrapper.count(), 1, dtype=np.float_))


print("Generating diagonal matricies...")
phis = data["phi"]
phisArray = np.ndarray(wrapper.count())
c = 0
for x in range(len(phis)):
	for y in range(len(phis[x])):
		if mask.get(x, y):
			phisArray[c] = math.pi - phis[x][y]
			c += 1
if c != len(phisArray):
	raise RuntimeError("REALLY?!?!?!?!?")
Ac = sparse.diags(-np.cos(phisArray))
As = sparse.diags(np.sin(phisArray))
Ik = sparse.identity(wrapper.count())

print("Generating A matrix...")
S = data["l"]
modS = math.sqrt(S[0]*S[0] + S[1]*S[1] + S[2]*S[2])
S[0] = S[0]/modS
S[1] = S[1]/modS
S[2] = S[2]/modS
A = sparse.vstack((
	sparse.hstack((Ac, As)),
	sparse.hstack((Ik.multiply(-S[0]), Ik.multiply(-S[1]))),
), format="csc")

print("Generating b vector...")
b = np.zeros(2*wrapper.count())
Iun = data["Iun"]
rho = data["rho"]
c = wrapper.count()
ri = 1.5
def f(p, n):
	return math.sqrt(
		( (n**4)*(1-p*p) + 2*n*n*(2*p*p+p-1) + p*p + 2*p - 4*(n**3)*p*math.sqrt(1-p*p) + 1 )
		/ ( ((p+1)**2)*((n**4) + 1) + 2*n*n*(3*p*p+2*p-1) )
	)
for x in range(len(phis)):
	for y in range(len(phis[x])):
		if mask.get(x, y):
			b[c] = Iun[x][y]/f(rho[x][y], ri) - S[2]
			c += 1

heights = lsqr(A, b, iter_lim=1000, show=True)[0]

print("Plotting...")
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
layout = plotly.graph_objs.Layout(title="RABBIT!!!")
fig = plotly.graph_objs.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename="output.html")
