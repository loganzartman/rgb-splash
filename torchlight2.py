import sys
import time
import random
from splash import *

INTENSITY = 0.5
if len(sys.argv) > 1:
	INTENSITY = float(sys.argv[1])

GRAVITY = -0.02
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

	def render(self, x, y):
		dx = x - self.x
		dy = y - self.y
		d = math.sqrt(dx**2 + dy**2)/self.r
		return IColor(max(0,1-d*3), max(0,0.7-d*4), max(0,0.3-d*5))

particles = [Particle(0.5,0.5)]

def render(x,y,img):
	# color = IColor(.12,.02,0)
	color = IColor()
	for p in particles:
		color += p.render(x,y)
	return color

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()
	
	img = Image(LED_W, LED_H)
	t0 = time.clock()

	while True:
		t0 = time.clock()
		if len(particles) < 3:
			particles.append(Particle(0.5,1.2))

		for p in particles:
			p.update()
			if not p.inBounds():
				particles.remove(p)

		img.compute(render)
		showImage(strip, img)
		
		dt = time.clock() - t0
		# print dt
		time.sleep(3./1000)
