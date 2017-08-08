import aiohttp
import asyncio
import async_timeout
import json

URL = "http://localhost:8080"

def logCallback(s):
	print("Received: " + str(s))

async def fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

async def fetchJSON(session, url):
	text = await fetch(session, url)
	return json.loads(text)

class Subscription:
	def __init__(self, session, path="/", callback=None):
		self.session = session
		self.path = path
		self.callback = callback

	async def subscribe(self):
		data = await fetchJSON(self.session, URL + self.path)
		if data["ok"]:
			if self.callback != None:
				self.callback(data)
		await self.subscribe()

async def main():
	async with aiohttp.ClientSession() as session:
		subs = []
		subs.append(Subscription(session, path="/test", callback=logCallback))
		subs.append(Subscription(session, path="/power", callback=logCallback))

		await asyncio.wait([sub.subscribe() for sub in subs])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())