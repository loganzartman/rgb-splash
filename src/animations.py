from splash.matrix import *
from splash.timer import *

class Animation:
	def __init__(self, strip):
		"""Construct an Animation Controller.
		strip -- a Neopixel LED strip to control
		"""
		self.strip = strip
		self.timer = FrameTimer(fps=60)
		self.img = Image(LED_W, LED_H)
		self.duration = None
		self.active = False
		self.onComplete = None
		self._animFunc = None

	def update(self):
		"""Update the LED strip with the current frame of animation."""
		if self._animFunc is None:
			return

		self.timer.startFrame()
		
		# see if animation is compelete
		if (self.timer.time > self.duration):
			self.active = False
			self._animFunc = None
			if self.onComplete is not None:
				self.onComplete()
			return

		self.img.compute(self._animFunc)
		showImage(self.strip, self.img)
		self.timer.endFrame()

	def startAnimation(self, func, duration=1, callback=None):
		"""Begin an animation given a render function."""
		self.timer.reset()
		self.duration = duration
		self.active = True
		def wrapped(x,y,img):
			return func(x,y,img,self.timer.time,self.duration)
		self._animFunc = wrapped
		self.onComplete = callback

	@staticmethod
	def colorWipeReverse(colorFrom, colorTo, duration=1, sharpness=1):
		return Animation.colorWipe(colorFrom, colorTo, sharpness, True)

	@staticmethod
	def colorWipe(colorFrom, colorTo, sharpness=1, reverse=False):
		m = -1. if reverse else 1.
		def render(x,y,img,t,duration):
			f = clip(-1*m + y + t/duration*2*m, 0, 1)
			if reverse:
				f = 1-f
			return colorFrom * (1-f) + colorTo * f

		return render

	@staticmethod
	def colorFade(colorFrom, colorTo):
		def render(x,y,img,t,duration):
			f = clip(t/duration, 0, 1)
			return colorFrom * (1-f) + colorTo * f

		return render
