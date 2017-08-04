from __future__ import print_function
import sys
import time
import random
import colorsys
from splash import *
from noise import *

t = 0
noise = Noise()

INTENSITY = 1.0
if len(sys.argv) > 1:
	INTENSITY = float(sys.argv[1])
BRIGHTNESS = INTENSITY

def render(x,y,img):
	global noise
	v = noise.perlin(x*.5,y*.5,1+t)
	rgb = colorsys.hls_to_rgb(v,.5,1.)
	return IColor(rgb[0], rgb[1], rgb[2])

def run():
	global t
	t0 = time.clock()

	strip = createStrip()
	img = Image(LED_W, LED_H)

	while True:
		t1 = time.clock()	
		
		t = time.clock() - t0
		img.compute(render)
		showImage(strip, img)
		
		dt = time.clock() - t1
		time.sleep(max(0, 32./1000 - dt))

# Main program logic follows:
if __name__ == '__main__':
	try:
		run()
	except KeyboardInterrupt:
		pass
