def normalizex(k):
	t = 0
	center = (len(k)-1)/2
	for y in range(len(k)):
		for x in range(len(k[y])):
			if y != center:
				k[y][x] /= abs(y-center)
				t += abs(k[y][x])
	for y in range(len(k)):
		for x in range(len(k[y])):
			k[y][x] /= t
	return k

def normalizey(k):
	t = 0
	center = (len(k)-1)/2
	for y in range(len(k)):
		for x in range(len(k[y])):
			if x != center:
				k[y][x] /= abs(x-center)
				t += abs(k[y][x])
	for y in range(len(k)):
		for x in range(len(k[y])):
			k[y][x] /= t
	return k
