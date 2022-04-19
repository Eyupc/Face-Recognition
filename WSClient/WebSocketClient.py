import asyncio
import json
import threading
import websocket

import websocket
class WebSocketClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name="WebSocketClient")


    def run(self):
        websocket.enableTrace(True)
        self.websocket = websocket.WebSocketApp("ws://10.3.41.25:8888",
                                                on_message=lambda ws, msg: self.on_message(ws, msg),
                                                on_error=lambda ws, msg: self.on_error(ws, msg),
                                                on_close=lambda ws: self.on_close(ws),
                                                on_open=lambda ws: self.on_open(ws))
        self.ws = None
        self.wst = threading.Thread(target=self.websocket.run_forever)
        self.wst.daemon = True
        self.wst.start()

    def on_open(self,ws):
        self.ws = ws

    def on_message(self,ws,message):
        pass

    def on_error(self,ws,error):
        pass

    def on_close(self,ws):
        pass

    def sendMessage(self,msg):
        if self.ws is None:
            return
        self.ws.send(msg)

