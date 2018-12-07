#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
import os

from tornado.options import options, define
define("port", default=8000, help="running on the given port", type="int")

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html",
		header_text="Header goes here",
		footer_text="Footer goes here")


if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r'/', IndexHandler)],
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	debug = True)
	httpserver = tornado.httpserver.HTTPServer(app)
	httpserver.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

