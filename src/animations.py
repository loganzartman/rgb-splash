from splash.matrix import *
from splash.timer import *

def timeWrapper(func, timer):
	def wrapped(x,y,img):
		return func(x,y,img,timer.time)
	return wrapped

def animate(strip, renderFunc, duration):
	timer = FrameTimer(fps=60)
	img = Image(LED_W, LED_H)
	wrapped = timeWrapper(renderFunc, timer)
	while (timer.time < duration):
		timer.startFrame()
		img.compute(wrapped)
		showImage(strip, img)
		timer.endFrame()

def colorWipeReverse(strip, colorFrom, colorTo, duration=1, sharpness=1):
	colorWipe(strip, colorFrom, colorTo, duration, sharpness, True)

def colorWipe(strip, colorFrom, colorTo, duration=1, sharpness=1, reverse=False):
	m = -1. if reverse else 1.
	def render(x,y,img,t):
		f = clip(-1*m + y + t/duration*2*m, 0, 1)
		if reverse:
			f = 1-f
		return colorFrom * (1-f) + colorTo * f

	animate(strip, render, duration)

def colorFade(strip, colorFrom, colorTo, duration=1):
	def render(x,y,img,t):
		f = clip(t/duration, 0, 1)
		return colorFrom * (1-f) + colorTo * f

	animate(strip, render, duration)
