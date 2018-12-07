#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import os.path


from tornado.options import options, define
define("port", default=8000, help="running on the given port", type="int")


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")



class HelloModule(tornado.web.UIModule):
	def render(self):
		return "<h1>Hello, World!</h1>"


if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(
			handlers = [(r'/', MainHandler),],
			template_path = os.path.join(os.path.dirname("__file__"), "templates"),
			ui_modules = {"Hello": HelloModule},
			debug = True)

	httpserver  = tornado.httpserver.HTTPServer(app)
	httpserver.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()