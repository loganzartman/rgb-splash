from splash.matrix import *
from client import *
import json

URL = "http://192.168.1.136:8080"
CID = "test"

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
		print(self.data)
		self.updateMatrix()

	def updateMatrix(self):
		bright = IColor(self.data["color"][0], self.data["color"][1], self.data["color"][2])
		dark = IColor()
		clear(self.strip, bright if self.data["power"] else dark)

def logWrap(callback):
	def f(data):
		print(data)
		callback(data)
	return f

tc = TestClient()
subs = []
# subs.append(Subscription(path="/test", callback=logCallback))
subs.append(Subscription(path="/client/"+CID+"/state/power", callback=tc.copyUpdateCallback))
subs.append(Subscription(path="/client/"+CID+"/state/color", callback=tc.copyUpdateCallback))
print("Starting client...")
startClient(subs, URL, CID)
