import sys
from splash import *

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
