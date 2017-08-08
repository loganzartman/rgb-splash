import aiohttp
import asyncio
import async_timeout
import json

URL = None
CID = None

def logCallback(s):
	print("Received: " + str(s))

@asyncio.coroutine
def fetch(session, url):
	response = yield from session.get(url)
	return (yield from response.text())

@asyncio.coroutine
def fetchJSON(session, url):
	text = yield from fetch(session, url)
	return json.loads(text)

class Subscription:
	def __init__(self, path="/", callback=None):
		self.session = None
		self.path = path
		self.callback = callback

	@asyncio.coroutine
	def subscribe(self):
		data = yield from fetchJSON(self.session, URL + self.path)
		if data["ok"]:
			if self.callback != None:
				self.callback(data)
		yield from self.subscribe()

@asyncio.coroutine
def main(subs):
	session = aiohttp.ClientSession()
	for sub in subs:
		sub.session = session
	yield from fetchJSON(session, URL+"/client/"+CID+"/connect")
	yield from asyncio.wait([sub.subscribe() for sub in subs])

def startClient(subs, url, cid):
	global URL
	global CID
	URL = url
	CID = cid	
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(subs))
