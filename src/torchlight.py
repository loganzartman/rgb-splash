import time
import math
import random
from splash.matrix import *

t0 = time.clock()
t = 0

def gradient(x,y,img):
	#compute center
	cx = .5
	cy = .5
	cx += math.sin(t*3.2)*0.1
	cy += math.cos(t*7.2)*0.2 + math.cos(t*11.12)*0.1
	cx += random.gauss(0,0.05)
	cy += random.gauss(0,0.2)

	#compute distance
	dx = x - cx
	dy = y - cy
	dist = math.sqrt(dx**2 + dy**2)

	return IColor(1 - dist**2 - random.uniform(0, 0.3), 0.8 - dist*1.6, 0.4 - dist*3)

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()

	img = Image(LED_W, LED_H)

	while True:
		#update time
		t = t + (time.clock() - t0)
		t0 = time.clock()

		#compute pixels
		img.compute(gradient)
		showImage(strip, img)

		#wait
		time.sleep(16./1000)
