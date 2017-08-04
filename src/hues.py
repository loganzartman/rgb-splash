import sys
from splash import *

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()
	
	for i in range(LED_COUNT):
		h = float(i)/LED_COUNT
		strip.setPixelColor(i, IColor.fromHSL(h,1,0.25).pack())
	strip.show()
