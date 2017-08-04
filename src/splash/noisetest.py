from noise import *
import math
import time
import os
import sys
import ansi
import colorsys

WIDTH = 32
HEIGHT = 16
SCALE = 0.08
SPEED = 3
CHR = " "
colors = [ansi.COLOR_RED, ansi.COLOR_YELLOW, ansi.COLOR_GREEN, ansi.COLOR_CYAN, ansi.COLOR_BLUE, ansi.COLOR_BLACK]

noise = Noise()

def render(t=0):
	for y in range(0,HEIGHT):
		for x in range(0,WIDTH):
			val = noise.perlin(1+x*SCALE+t, 1+y*SCALE, 1+t) * 0.5 + 0.5
			rgb = colorsys.hls_to_rgb(val*2.,0.5,1.0)
			ansi.setColorRGB(255-rgb[0]*255, rgb[1]*255, rgb[2]*255, ansi.COLOR_BG)
			sys.stdout.write(CHR)
		sys.stdout.write("\n")
	sys.stdout.flush()

def rrt():
	t = 0
	t0 = time.clock()

	ansi.cursorHide()
	
	while True:
		t1 = time.clock()
		ansi.cursorLoad()
		render(t*SPEED)
		
		dt = time.clock() - t1
		t = time.clock() - t0
		time.sleep(max(0, 32./1000 - dt))

try:
	rrt()
except KeyboardInterrupt:
	ansi.resetFormat()
	ansi.cursorTo()
	ansi.clear()
	ansi.cursorShow()
	pass