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

timer = FrameTimer()
noise = Noise()

INTENSITY = 1.0
if len(sys.argv) > 1:
	INTENSITY = float(sys.argv[1])
BRIGHTNESS = INTENSITY

BH = 10

def renderNoise(x, y, img):
	global noise
	v = noise.perlin(x*.75,y*BH*.75,1)
	v = 1 - abs(v)
	v = v * v * v * v
	v = rangeClip(v,0.2,1.0,0.,1.)
	rgb = (v,v,v)
	return IColor(rgb[0], rgb[1], rgb[2])

def run():
	strip = createStrip()

	img = Image(LED_W, LED_H)

	nbuffer = Image(LED_W, LED_H*BH)
	nbuffer.compute(renderNoise)
	
	while True:
		timer.startFrame()

		img.clear()
		img.drawImage(nbuffer, 0, -math.fmod(timer.time, 10))
		img.drawImage(nbuffer, 0, 10-math.fmod(timer.time, 10))
		showImage(strip, img)
		print(timer.realFps)
		
		timer.endFrame()

# Main program logic follows:
if __name__ == '__main__':
	try:
		run()
	except KeyboardInterrupt:
		pass
