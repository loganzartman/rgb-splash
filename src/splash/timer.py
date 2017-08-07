import time

MIN_SLEEP = 1./1000

class FrameTimer:
	def __init__(self, fps=60):
		self.fps = float(fps)
		self.realFps = self.fps
		self.t0 = time.time()
		self.frameStart = self.t0
		self.time = 0

	def startFrame(self):
		self.frameStart = time.time()
		self.time = self.frameStart - self.t0

	def endFrame(self):
		dt = time.time() - self.frameStart
		self.realFps = 1/dt
		time.sleep(max(MIN_SLEEP, 1/self.fps - dt))