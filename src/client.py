import aiohttp
import asyncio
import async_timeout
import json
import signal

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
        asyncio.async(self.subscribe())

def doConnect():
    loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def connect():
        session = aiohttp.ClientSession()
        yield from fetchJSON(session, URL+"/client/"+CID+"/connect")
    loop.run_until_complete(connect())

@asyncio.coroutine
def main(subs, updateCallback):
    session = aiohttp.ClientSession()

    for sub in subs:
        sub.session = session
        print("Subscribing to " + sub.path + "...")
        asyncio.async(sub.subscribe())

def startClient(subs, url, cid, updateCallback=None):
    global URL
    global CID
    URL = url
    CID = cid

    loop = asyncio.get_event_loop()
    
    def updateWrapper():
        if updateCallback is not None:
            updateCallback()
        loop.call_soon(updateWrapper)
    
    try:
        doConnect()
        loop.call_soon(updateWrapper)
        loop.run_until_complete(main(subs, updateCallback))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except asyncio.CancelledError:
        print("Task cancelled.")
    finally:
        loop.close()