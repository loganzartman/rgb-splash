"""Continuously display a rainbow plasma effect."""

from __future__ import print_function
import sys
import time
import random
import colorsys
from splash.matrix import *
from splash.noise import *
from splash.timer import *

timer = FrameTimer()
noise = Noise()

INTENSITY = 1.0
if len(sys.argv) > 1:
	INTENSITY = float(sys.argv[1])
BRIGHTNESS = INTENSITY

def render(x,y,img):
	global noise
	t = timer.time
	v = noise.perlin(x*.5,y*.5,1+t)
	rgb = colorsys.hls_to_rgb(v,.5,1.)
	return IColor(rgb[0], rgb[1], rgb[2])

def run():
	strip = createStrip()
	img = Image(LED_W, LED_H)

	while True:
		timer.startFrame()

		img.compute(render)
		showImage(strip, img)
		
		timer.endFrame()

# Main program logic follows:
if __name__ == '__main__':
	try:
		run()
	except KeyboardInterrupt:
		pass
