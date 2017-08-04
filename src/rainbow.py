import time
import math
from random import randint
from splash import *

t0 = time.clock()
t = 0

def gradient(x,y,img):
	dr = (x - (0.5 + math.sin(t*4)*.7))**2
	dg = (x - (0.5 + math.sin(t*6.2)*.7))**2
	db = (x - (0.5 + math.sin(t*3.1)*.7))**2
	return IColor(1-dr*8, 1-dg*8, 1-db*8)

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()

	img = Image(LED_W, LED_H)

	while True:
		#update time
		t = t + (time.clock() - t0)
		t0 = time.clock()

		#compute pixels
		showImage(strip, img)
		img.compute(gradient)

		#wait
		time.sleep(8./1000)
