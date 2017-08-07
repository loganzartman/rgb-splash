"""Continuously display a torchlight effect.
Provide a single argument: intensity multiplier.
"""

import sys
import time
import random
from splash.matrix import *
from splash.timer import *
from splash.noise import *

timer = FrameTimer()
noise = Noise()

INTENSITY = 1.0
if len(sys.argv) > 1:
	INTENSITY = float(sys.argv[1])
BRIGHTNESS = INTENSITY

SCALE = 2
SPEED = 2

def render(x,y,img):
	t = timer.time
	v = noise.perlin(1+x*SCALE,2+y*SCALE+t*2,t)*0.5+0.5

	dx = (x - 0.5)*1.0
	dy = (y - 0.9)*0.5
	d = math.sqrt(dx*dx+dy*dy)

	return IColor(max(v-d, 0), max(v*0.8-d*1.4, 0), max(v*0.3-d*1.5, 0))

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()
	
	img = Image(LED_W, LED_H)

	while True:		
		timer.startFrame()

		img.compute(render)
		showImage(strip, img)
		
		timer.endFrame()
