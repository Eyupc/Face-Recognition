import asyncio
import json
import threading
from threading import Thread
from asyncio import sleep

import websockets

from ObjectsManager import ObjectsManager
from WS.WebSocketManager import WebSocketManager
from utils.TextConverter import TextConverter


class WebSocketServer(Thread):
    def __init__(self, address, port):
        Thread.__init__(self)
        self.port = port
        self.address = address
    def run(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ws_server = websockets.serve(self.ws_handler, self.address, self.port)
        loop.run_until_complete(ws_server)
        loop.run_forever()



    async def ws_handler(self, websocket, path):
        while True:
            try:
                result = await websocket.recv()
                data = json.loads(TextConverter.decodeBytes(bytes(result)))
                Event = ObjectsManager.getIncomingerManager().getEvent(data['header'])
                await Event(websocket,data['header'],data['data'][0]).execute()

            except websockets.ConnectionClosed:
                WebSocketManager.removeClient(websocket)
                print(f"User disconnected!")
                return

