"""Continuously display a bouncing ball."""

import time
import math
import random
from splash.matrix import *

t0 = time.clock()
t = 0

ball = dict(x=0.5, y=0.5, vx=0.03, vy=0.021)

def gradient(x,y,img):
	dx = x - ball["x"]
	dy = y - ball["y"]
	dist = math.sqrt(dx**2 + dy**2)
	return IColor(1-dist*16,0.8-dist*4,0.6-dist*7)

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()

	img = Image(LED_W, LED_H)

	while True:
		#update time
		t = t + (time.clock() - t0)
		t0 = time.clock()

		ball["x"] += ball["vx"]
		ball["y"] += ball["vy"]
		if ball["x"] > 1 or ball["x"] < 0:
			ball["vx"] = -ball["vx"]
		if ball["y"] > 1 or ball["y"] < 0:
			ball["vy"] = -ball["vy"]

		#compute pixels
		img.compute(gradient)
		showImage(strip, img)

		#wait
		time.sleep(16./1000)
