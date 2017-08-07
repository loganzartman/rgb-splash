import aiohttp
import asyncio
import async_timeout
import json

def logCallback(s):
	print("Received: " + s)

async def fetch(session, url):
	with async_timeout.timeout(10):
		async with session.get(url) as response:
			return await response.text()

async def fetchJSON(session, url):
	text = await fetch(session, url)
	return json.loads(text)

class Subscription:
	def __init__(self, session, path="/", callback=None):
		self.path = path
		self.callback = callback

async def main():
	async with aiohttp.ClientSession() as session:
		print("Waiting...")
		data = await fetchJSON(session, "http://localhost:8080/test")
		print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())