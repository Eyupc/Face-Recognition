import asyncio
import json
import multiprocessing
from asyncio import sleep
from multiprocessing import Process

import websockets

class WebSocketServer(multiprocessing.Process):
    def __init__(self, address, port):
        super().__init__()
        self.port = port
        self.address = address

    def run(self):
        loop = asyncio.new_event_loop()
        ws_server = websockets.serve(self.ws_handler, self.address, self.port,
                                     ping_timeout=None, ping_interval=None, loop=loop)
        loop.run_until_complete(ws_server)
        loop.run_forever()

    async def ws_handler(self, websocket, path):
        while True:
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
                break

ws = WebSocketServer("localhost",6969)
