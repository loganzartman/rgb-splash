"""Continuously display a moving metaball."""

import time
import math
from random import randint
from splash.matrix import *
from splash.timer import *

timer = FrameTimer(fps=60)

def gradient(x,y,img):
	t = timer.time
	dx = x - (0.5 + math.sin(t*4)*0.4)
	dy = y - (0.5 + math.cos(t*5.2)*0.4)
	dist = math.sqrt(dx**2 + dy**2)
	return IColor.fromHSL(t*.5+dist*.5, min(1, dist*3.2), max(0, 1-dist*2.2))

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()

	img = Image(LED_W, LED_H)

	while True:
		timer.startFrame()

		#compute pixels
		showImage(strip, img)
		img.compute(gradient)

		timer.endFrame()
