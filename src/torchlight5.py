import sys
import time
import random
from splash.matrix import *

t = 0
t0 = time.clock()

INTENSITY = 1.0
if len(sys.argv) > 1:
	INTENSITY = float(sys.argv[1])
BRIGHTNESS = INTENSITY

def render(x,y,img):
	cx = 0.5
	cx += math.sin(t*4+y)*.5*(1-y*.6)
	cx += math.sin(t*7+y*2)*.5*(1-y*.6)
	dx = x - cx

	oys = (math.sin(t*4.7)+1)*0.25+0.25
	oy = math.sin(t*21)*.025 * oys
	oy += math.sin(t*23+1.24)*.025 * oys
	oy += math.sin(t*37)*.05 * oys

	v = (1.1-abs(dx)*2)*max(0,y+oy)
	v = max(0, min(1, v)) * BRIGHTNESS
	return IColor(v + random.uniform(0,0.1),v**2*.65,v**6*.05)

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()
	
	img = Image(LED_W, LED_H)

	while True:		
		img.compute(render)
		showImage(strip, img)
		
		t += time.clock() - t0
		t0 = time.clock()
		time.sleep(10./1000)