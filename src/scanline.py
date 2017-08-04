import time
import math
from random import randint
from splash import *

t0 = time.clock()
t = 0

def gradient(x,y,img):
	v = y-1+(t)%2
	return IColor(v,v,v)

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
		time.sleep(16./1000)
