import time
import math
from random import randint
from splash.matrix import *
from splash.timer import *

timer = FrameTimer()

def gradient(x,y,img):
	t = timer.time
	v = y-1+(t)%2
	return IColor(v,v,v)

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
