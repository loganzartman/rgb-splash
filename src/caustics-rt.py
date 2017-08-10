"""Continuously display a rainbow plasma effect."""

from __future__ import print_function
import sys
import time
import random
import colorsys
import math
from splash.matrix import *
from splash.noise import *
from splash.timer import *

timer = FrameTimer(fps=12)
noise = Noise()

INTENSITY = 1.0
if len(sys.argv) > 1:
	INTENSITY = float(sys.argv[1])
BRIGHTNESS = INTENSITY

def renderNoise(x, y, img):
	global noise
	t = timer.time
	v = noise.fast3d(x*.75,y*.75+t*2,1)
	# v = 1 - abs(v)
	# v = v * v * v * v
	# v = rangeClip(v,0.3,1.0,0.,1.)
	rgb = (v,v,v)
	return IColor(rgb[0], rgb[1], rgb[2])

def run():
	strip = createStrip()

	img = Image(LED_W, LED_H)
	
	while True:
		timer.startFrame()

		img.compute(renderNoise)
		showImage(strip, img)
		print(timer.realFps)
		
		timer.endFrame()

# Main program logic follows:
if __name__ == '__main__':
	try:
		run()
	except KeyboardInterrupt:
		pass
