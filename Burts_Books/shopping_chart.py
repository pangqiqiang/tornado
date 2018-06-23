#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from uuid import uuid4
import json

from tornado.options import define, options
define("port", default=8000, type=int, help="running on the given port")


class ShoppingCart:
    totalInventory = 10
    callbacks = []
    carts = {}

    def register(self, callback):
        self.callbacks.append(callback)

    def moveItemToCart(self, session):
        if session in self.carts:
            return
        self.carts[session] = True
        self.notifyCallbacks()

    def removeItemFromCart(self, session):
        if session not in self.carts:
            return
        del self.carts[session]
        self.notifyCallbacks()

    def notifyCallbacks(self):
        for c in self.callbacks:
            self.callbackHelper(c)
        self.callbacks = []

    def callbackHelper(self, callback):
        callback(self.getInventoryCount())

    def getInventoryCount(self):
        return self.totalInventory - len(self.carts)


class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        session = uuid4()
        count = self.application.ShoppingCart.getInventoryCount()
        self.render("index.html", session=session, count=count)


class CartHandler(tornado.web.RequestHandler):
    def post(self):
        action = self.get_argument('action')
        session = self.get_argument('session')
        if not session:
            self.set_status(400)
            return
        if action == 'add':
            self.application.ShoppingCart.moveItemToCart(session)
        elif action == 'remove':
            self.application.ShoppingCart.removeItemFromCart(session)
        else:
            self.set_status(400)


class StatusHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.application.ShoppingCart.register(self.on_message)

    def on_message(self, count):
        self.write('{"inventoryCount": %d}' % count)
        self.finish()


class Application(tornado.web.Application):
    def __init__(self):
        self.ShoppingCart = ShoppingCart()
        handlers = [
            (r'/', DetailHandler),
            (r'/cart', CartHandler),
            (r'/cart/status', StatusHandler)
        ]
        settings = {
            'template_path': 'templates',
            'static_path': 'static',
            'debug': True
        }
        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = Application()
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
