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
		self.continuous = False
		self.onComplete = None
		self._animFunc = None

	def update(self):
		"""Update the LED strip with the current frame of animation."""
		if self._animFunc is None:
			return

		self.timer.startFrame()
		
		# see if animation is compelete
		if (not self.continuous and self.timer.time > self.duration):
			self.active = False
			self._animFunc = None
			if self.onComplete is not None:
				self.onComplete(True)
			return

		self.img.compute(self._animFunc)
		showImage(self.strip, self.img)
		self.timer.endFrame()

	def startAnimation(self, func, duration=1, callback=None):
		"""Begin an animation given a render function."""
		if self.active:
			if self.onComplete is not None:
				self.onComplete(False)

		self.timer.reset()
		self.duration = duration
		self.active = True
		self.continuous = False
		def wrapped(x,y,img):
			return func(x,y,img,self.timer.time,self.duration)
		self._animFunc = wrapped
		self.onComplete = callback

	def startContinuous(self, func):
		self.startAnimation(func)
		self.duration = None
		self.continuous = True

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

	@staticmethod
	def strobe(color, speed):
		def render(x,y,img,t,duration):
			v = math.sin(t*speed)
			return color * v

		return render

	@staticmethod
	def twinkle(color, speed):
		def render(x,y,img,t,duration):
			v = math.sin(t*speed)
			return color * v

		return render

	@staticmethod
	def rainbow(speed):
		def render(x,y,img,t,duration):
			O = math.pi / 3.
			return IColor(math.sin(x+t*speed), math.sin(x+t*speed+O), math.sin(x+t*speed+O*2))

		return render
