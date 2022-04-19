import json
import threading

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket as ws
from tornado.options import define, options

from WS.WebSocketManager import WebSocketManager
from WS.incoming.IManager import IncomingManager
from utils.TextConverter import TextConverter

define('port', default=7777, help='Websocket Server Port')
class WebSocketHandler(ws.WebSocketHandler):

    __incomingManager = IncomingManager()
    @classmethod
    def route_urls(cls):
        return [(r'/', cls, {}), ]

    def open(self):
        print("[WS] New client connected!")

    async def on_message(self, message):
        data = json.loads(TextConverter.decodeBytes(bytes(message)))
        Event = WebSocketHandler.__incomingManager.getEvent(data['header'])
        Event(self, data['header'], data['data'][0]).execute()
    def on_close(self):
        WebSocketManager.removeClient(self)
        print("[WS] WS-Client disconnected")

    def check_origin(self, origin):
        return True


class WebSocketServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name='WebServer')
        self.ioloop = None

    def run(self):
        self.ioloop = tornado.ioloop.IOLoop()
        app = tornado.web.Application(WebSocketHandler.route_urls())
        server = tornado.httpserver.HTTPServer(app)
        server.listen(options.port)
        self.ioloop.start()
        self.ioloop.clear_instance()

    def stop(self):
        self.ioloop.add_callback(self.ioloop.stop)

