import sys
from splash.matrix import *

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()
	
	n = len(sys.argv)
	t = 2000
	b = 1.

	if n >= 2:
		t = float(sys.argv[1])
	if n >= 3:
		b = float(sys.argv[2])
	
	clear(strip, IColor.fromKelvin(t) * b)
