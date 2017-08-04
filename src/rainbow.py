import time
import math
from random import randint
from splash.matrix import *
from splash.timer import *

timer = FrameTimer()

def gradient(x,y,img):
	t = timer.time
	dr = (x - (0.5 + math.sin(t*4)*.7))**2
	dg = (x - (0.5 + math.sin(t*6.2)*.7))**2
	db = (x - (0.5 + math.sin(t*3.1)*.7))**2
	return IColor(1-dr*8, 1-dg*8, 1-db*8)

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