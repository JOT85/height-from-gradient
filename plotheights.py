import plotly
import numpy as np

def toMap(mask, heights):
	out = np.full((mask.width(), mask.height()), np.NaN, dtype=np.float_)
	c =  0
	for x in range(mask.width()):
		for y in range(mask.height()):
			if mask.get(x, y):
				out[x][y] = heights[c]
				c += 1
	return out

def plot(heights, mask, title="Depth map", file="output.html"):
	data = [plotly.graph_objs.Surface(z=toMap(mask, heights))]
	layout = plotly.graph_objs.Layout(title=title)
	fig = plotly.graph_objs.Figure(data=data, layout=layout)
	plotly.offline.plot(fig, filename=file)
