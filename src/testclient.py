from splash.matrix import *
from client import *
import json
from animations import Animation
import sys

URL = "http://localhost:8080"
CID = "test-client"

if len(sys.argv) == 2:
	URL = sys.argv[1]

class TestClient:
	def __init__(self):
		self.strip = createStrip()
		self.animation = Animation(self.strip)
		with open("defaults.json", "r") as file:
			self.data = json.loads(file.read())

	def copyCallback(self, data):
		for k,v in data.items():
			if k != "ok":
				self.data[k] = v

	def copyUpdateCallback(self, data):
		self.copyCallback(data)
		self.updateMatrixColor()

	def animationComplete(self, completed):
		self.updateMatrixColor()

	def powerCallback(self, data):
		previousPower = self.getPower()
		self.copyCallback(data)
		color = self.getColor()
		black = IColor()
		fromColor = color if previousPower else black
		toColor = color if self.getPower() else black
		
		f = None
		if not self.getPower():
			f = Animation.colorWipeReverse(fromColor, toColor)
		else:
			f = Animation.colorWipe(fromColor, toColor)
		self.animation.startAnimation(f, 0.5, self.animationComplete)

	def colorCallback(self, data):
		previousColor = self.getColor()
		self.copyCallback(data)
		color = self.getColor()
		if self.getPower():
			f = Animation.colorFade(previousColor, color)
			self.animation.startAnimation(f, 0.1, self.animationComplete)

	def actionCallback(self, data):
		if data["action"] == "anim-strobe":
			f = Animation.strobe(self.getColor(), 5)
			self.animation.startContinuous(f)
		elif data["action"] == "anim-twinkle":
			f = Animation.twinkle(self.getColor(), 2)
			self.animation.startContinuous(f)
		elif data["action"] == "anim-rainbow":
			f = Animation.rainbow(3)
			self.animation.startContinuous(f)

	def update(self):
		if self.animation.active:
			self.animation.update()
		else:
			self.animation.timer.startFrame()
			self.animation.timer.endFrame()

	def updateMatrixColor(self):
		bright = self.getColor()
		dark = IColor()
		clear(self.strip, bright if self.getPower() else dark)

	def getColor(self):
		return IColor(self.data["color"][0], self.data["color"][1], self.data["color"][2])

	def getPower(self):
		return self.data["power"]

def logWrap(callback):
	def f(data):
		print(data)
		callback(data)
	return f

tc = TestClient()
subs = []
# subs.append(Subscription(path="/test", callback=logCallback))
subs.append(Subscription(path="/client/"+CID+"/state/power", callback=tc.powerCallback))
subs.append(Subscription(path="/client/"+CID+"/state/color", callback=tc.colorCallback))
subs.append(Subscription(path="/client/"+CID+"/state/action", callback=tc.actionCallback))
print("Starting client...")
startClient(subs, URL, CID, tc.update)
