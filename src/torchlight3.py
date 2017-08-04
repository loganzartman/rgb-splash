"""Continuously display a torchlight effect.
Provide a single argument: intensity multiplier.
"""

import sys
import time
import random
from splash.matrix import *

INTENSITY = 0.5
if len(sys.argv) > 1:
	INTENSITY = float(sys.argv[1])

GRAVITY = -0.01
DECAY = 0.7 + INTENSITY * (0.3)

class Particle:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.vx = random.gauss(0,0.03)
		self.vy = random.uniform(-0.1, 0.05)
		self.r = random.uniform(2,2.2)

	def update(self):
		self.x += self.vx
		self.y += self.vy
		self.vy += GRAVITY
		self.r *= DECAY

	def inBounds(self):
		return self.x >= 0 and self.y >= 0 and self.x <= 1

	def render(self, img):
		ix = int(math.floor(self.x * img.w))
		iy = int(math.floor(self.y * img.h))
		color = img.getPixel(ix, iy)
		img.setPixel(ix, iy, color + IColor(.2,.04,.00))

particles = [Particle(0.5,0.5)]

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()
	
	img = Image(LED_W, LED_H)
	t0 = time.clock()

	while True:
		t0 = time.clock()
		if len(particles) < 70:
			particles.append(Particle(0.5,1.2))

		img.clear()
		for p in particles:
			p.update()
			if not p.inBounds():
				particles.remove(p)
			else:
				p.render(img)

		showImage(strip, img)
		
		dt = time.clock() - t0
		# print dt
		time.sleep(10./1000)