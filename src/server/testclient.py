from splash.matrix import *
from client import *

URL = "http://192.168.1.136:8080"
CID = "test"

class TestClient:
	def __init__(self):
		self.strip = createStrip()
		self.power = False
		self.bright = IColor(1,.5,.1)
		self.dark = IColor()

	def powerCallback(self, data):
		self.power = data["power"]
		self.updateMatrix()

	def colorCallback(self, data):
		self.bright = IColor(data["color"][0], data["color"][1], data["color"][2])
		self.updateMatrix()

	def updateMatrix(self):
		clear(self.strip, self.bright if self.power else self.dark)

tc = TestClient()
subs = []
subs.append(Subscription(path="/test", callback=logCallback))
subs.append(Subscription(path="/client/"+CID+"/state/power", callback=tc.powerCallback))
subs.append(Subscription(path="/client/"+CID+"/state/color", callback=tc.colorCallback))
startClient(subs, URL, CID)
