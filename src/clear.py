"""Immediately clear the matrix to black, a grayscale value, or an RGB color.
If a single argument is passed:
It is interpreted as a grayscale float in the range [0,1]

If three arguments are passed:
They are intepreted as red, green, and blue floats in the range [0,1]
"""

import sys
from splash.matrix import *

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()


	n = len(sys.argv)
	r = g = b = 0

	if n == 2:
		r = g = b = float(sys.argv[1])
	elif n == 4:
		r = float(sys.argv[1])
		g = float(sys.argv[2])
		b = float(sys.argv[3])
	
	clear(strip, IColor(r,g,b))
