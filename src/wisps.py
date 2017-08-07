"""Continuously display a wisp effect.
Provide a single argument: intensity multiplier.
"""

import sys
import time
import random
from splash.matrix import *
from splash.timer import *

timer = FrameTimer()

INTENSITY = 0.5
if len(sys.argv) > 1:
	INTENSITY = float(sys.argv[1])

GRAVITY = 0

class Particle:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.vx = 0
		self.vy = random.uniform(-0.05, -0.03)
		self.color = IColor.fromHSL(random.uniform(0,1), 1.0, 0.5)

	def update(self):
		self.x += self.vx
		self.y += self.vy
		self.vy += GRAVITY

	def inBounds(self):
		return self.x >= 0 and self.y >= 0 and self.x <= 1

	def render(self, img):
		ip = (self.x * img.w, self.y * img.h)
		ip0 = (int(math.floor(ip[0])), int(math.floor(ip[1])))
		ip1 = (int(math.floor(ip[0])), int(math.ceil(ip[1])))
		f = ip[1]%1.

		color0 = img.getPixel(ip0[0], ip0[1])
		color1 = img.getPixel(ip1[0], ip1[1])
		img.setPixel(ip0[0], ip0[1], color0 + self.color * (1-f))
		img.setPixel(ip1[0], ip1[1], color1 + self.color * f)

particles = [Particle(0.5,0.5)]

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()
	
	img = Image(LED_W, LED_H)
	t0 = time.clock()

	while True:
		timer.startFrame()

		if len(particles) < 3:
			particles.append(Particle(random.uniform(0,1),1.2))

		img.clear()
		for p in particles:
			p.update()
			if not p.inBounds():
				particles.remove(p)
			else:
				p.render(img)

		showImage(strip, img)
		
		timer.endFrame()