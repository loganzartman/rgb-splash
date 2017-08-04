import time
from splash.matrix import *

idx = 0

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()
	
	t0 = time.clock()
	
	while True:
		clear(strip)
		strip.setPixelColor(idx, IColor(0,0,1).pack())
		strip.show()

		idx += 1
		if idx >= LED_COUNT:
			print("FPS: "+str(LED_COUNT/float(time.clock()-t0)))
			t0 = time.clock()
			idx = 0

		time.sleep(32./1000)
