# height-from-gradient

Utilities for creating a heightmap from a set of known gradients.
Along with utilities for testing the effectiveness of different kernels.

## m module
Provides:
	applyKernels - Generates a matrix that applys the given kernels to a vector of values.
	createHeightNormMatrix - Creates a matrix to normalise the height values when solving.
	maskwrapper - A class that provides utilities around a mask.
	normalise - Returns the given vector, however with the values averaging at 0.

## testrunner module
Provides:
	compareValues - Returns the average squared difference of each value in the given arrays.
	testFunction - Measures the accuracy of the solved height values. See its docstring for more details.

## generator module
Provides:
	fromFunction - Creates a plain, vector, and mask of heights and gradients from a given function.
	toVector - Takes a map and mask, and creates a vector of all the values of map that are within the mask.

# Kernel interface
size(): Kernels must be square, therefore size is the width or height.
get(x, y): Returns the value of the kernel at coordinate (x, y), with the top left being (0, 0)
## kernel module
Provides:
	kernel class to wrap kernel array
## testkernels module
Provides:
	Some basic kernels:
		xkernels - Kernels for finding the x gradient
		ykernels - Kernels for finding the y gradient
		kernels - A list containing all kernels

# Mask interface
width(): Returns the width of the mask.
height(): Returns the height of the mask.
get(x, y): Returns a boolean, True if the coordinate is within the mask.
set(x, y, v): Sets the value of the mask at (x, y) to the boolean v.
## arraymask module
Provides:
	mask class that contains a 2D array of booleans, interfaced as a mask.
## alltruemask module
Provides:
	mask class that implements the mask interface and all values within its size return true.

# matrix interface
get(x, y, v): Sets (x, y) in the matrix to v
resize(w, h): Resizes the matrix to the given width an height
width(): Returns the width of the matrix (the amount of columns)
height(): Returns the height of the matrix (the amount of rows)

## sparsematrix module
Provides:
	matrix class implements the matrix interface around scipy.sparse.lil_matrix
