import sys
from splash.matrix import *

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()
	
	n = len(sys.argv)
	r = 1.
	g = 1.
	b = 1.

	if n == 2:
		r = float(sys.argv[1])
		g = r
		b = r
	if n == 4:
		r = float(sys.argv[1])
		g = float(sys.argv[2])
		b = float(sys.argv[3])

	ar = 0
	ag = 0
	ab = 0

	for i in range(LED_COUNT):
		vr = vg = vb = 0
		ar += r
		ag += g
		ab += b
		if ar >= 1:
			ar -= 1
			vr = 1
		if ag >= 1:
			ag -= 1
			vg = 1
		if ab >= 1:
			ab -= 1
			vb = 1
		strip.setPixelColor(i, IColor(vr,vg,vb).pack())
	strip.show()
