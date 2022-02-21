import json
import threading

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket as ws
from tornado.options import define, options

from ObjectsManager import ObjectsManager
from WS.WebSocketManager import WebSocketManager
from utils.TextConverter import TextConverter

define('port', default=7777, help='port to listen on')
class WebSocketHandler(ws.WebSocketHandler):

    LAST_IMAGE = None
    @classmethod
    def route_urls(cls):
        return [(r'/', cls, {}), ]

    def open(self):
        print("New client connected")

    def on_message(self, message):
        data = json.loads(TextConverter.decodeBytes(bytes(message)))
        Event = ObjectsManager.getIncomingerManager().getEvent(data['header'])
        Event(self, data['header'], data['data'][0]).execute()

    def on_close(self):
        WebSocketManager.removeClient(self)
        print("connection is closed")

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

