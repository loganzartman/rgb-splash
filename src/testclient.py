from splash.matrix import *
from client import *
import json
import animations
import sys

URL = "http://localhost:8080"
CID = "test"

if len(sys.argv) == 2:
	URL = sys.argv[1]

class TestClient:
	def __init__(self):
		self.strip = createStrip()
		with open("defaults.json", "r") as file:
			self.data = json.loads(file.read())

	def copyCallback(self, data):
		for k,v in data.items():
			if k != "ok":
				self.data[k] = v

	def copyUpdateCallback(self, data):
		self.copyCallback(data)
		self.updateMatrix()

	def powerCallback(self, data):
		previousPower = self.getPower()
		self.copyCallback(data)
		color = self.getColor()
		black = IColor()
		fromColor = color if previousPower else black
		toColor = color if self.getPower() else black
		if not self.getPower():
			animations.colorWipeReverse(self.strip, fromColor, toColor, 0.5, 2)
		else:
			animations.colorWipe(self.strip, fromColor, toColor, 0.5, 2)

	def colorCallback(self, data):
		previousColor = self.getColor()
		self.copyCallback(data)
		color = self.getColor()
		if self.getPower():
			animations.colorFade(self.strip, previousColor, color, 0.1)

	def updateMatrix(self):
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
print("Starting client...")
startClient(subs, URL, CID)
