
# -*- coding: utf-8 -*-

from noise import *
import math
import time
import os
import sys
import ansi
import colorsys

def clear():
	os.system("cls" if os.name == "nt" else "clear")

WIDTH = 40
HEIGHT = 15
SCALE = 0.05
SPEED = 2
CHR = "█"
colors = [ansi.COLOR_RED, ansi.COLOR_YELLOW, ansi.COLOR_GREEN, ansi.COLOR_CYAN, ansi.COLOR_BLUE, ansi.COLOR_BLACK]

noise = Noise()

def render(t=0):
	for y in range(0,HEIGHT):
		for x in range(0,WIDTH):
			val = noise.perlin(1+x*SCALE+t, 1+y*SCALE, 1+t) * 0.5 + 0.5
			rgb = colorsys.hls_to_rgb(val,0.5,1.0)
			ansi.setColorRGB(rgb[0]*255, rgb[1]*255, rgb[2]*255)
			sys.stdout.write(CHR)
		sys.stdout.write("\n")
	sys.stdout.flush()

def rrt():
	t = 0
	t0 = time.clock()
	
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
	pass