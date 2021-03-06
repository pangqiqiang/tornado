#!/usr/bin/env python
#-*-coding:utf-8-*-

import textwrap
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options

from tornado.options import define, options
define("port", default=8000, help="running on the given port", type=int)

class ReverseHandler(tornado.web.RequestHandler):
	def get(self, word):
		self.write(word[::-1])



class WrapHandler(tornado.web.RequestHandler):
	def post(self):
		text = self.get_argument("text")
		width = self.get_argument("width", 40)
		self.write(textwrap.fill(text, int(width)))


if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[(r'/reverse/(\w+)', ReverseHandler),
		(r'/wrap',WrapHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()
