from __future__ import print_function
import sys
import time
import random
from splash import *
from noise import *

t = 0

INTENSITY = 1.0
if len(sys.argv) > 1:
	INTENSITY = float(sys.argv[1])
BRIGHTNESS = INTENSITY

def render(x,y,img):
	return IColor(x,(y+t)%1,random.uniform(0,.01))

def run():
	t0 = time.clock()

	strip = createStrip()
	img = Image(LED_W, LED_H)

	while True:
		t1 = time.clock()	
		
		print("step")
		img.compute(render)
		showImage(strip, img)
		
		t = time.clock() - t0
		dt = time.clock() - t1
		time.sleep(max(0, 32./1000 - dt))

# Main program logic follows:
if __name__ == '__main__':
	try:
		run()
	except KeyboardInterrupt:
		pass
