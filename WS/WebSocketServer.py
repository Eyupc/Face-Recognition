import asyncio
import json
import threading
from threading import Thread
from asyncio import sleep

import websockets

class WebSocketServer(Thread):
    def __init__(self, address, port):
        Thread.__init__(self)
        self.port = port
        self.address = address
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ws_server = websockets.serve(self.ws_handler, self.address, self.port)
        loop.run_until_complete(ws_server)
        loop.run_forever()


    async def ws_handler(self, websocket, path):
        # simulate work
        print("doing some work")
        await sleep(5)
        print("Sending data")
        data = json.dumps({"test": "test test"})
        try:
            await websocket.send(data)
            result = await websocket.recv()
            print(result)
            result = json.loads(result)
            print(f"json: {result}")
        except websockets.ConnectionClosed:
            print(f"Terminated")
            return

ws = WebSocketServer("localhost",6969)
thr = Thread(target=ws.run,daemon=True)
thr.start()
while True:
    print('aaa')

