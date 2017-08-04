"""Test the framerate achievable by the matrix."""

import time
from splash.matrix import *

idx = 0

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()
	
	t0 = time.time()
	
	while True:
		clear(strip)
		strip.setPixelColor(idx, IColor(0,0,1).pack())
		strip.show()

		idx += 1
		if idx >= LED_COUNT:
			print("FPS: "+str(LED_COUNT/(time.time()-t0)))
			t0 = time.time()
			idx = 0

		time.sleep(0./1000)
