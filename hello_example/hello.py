#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options


from tornado.options import define, options
define("port", default=8000, help="running on the given port")

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		greeting = self.get_argument("greeting", "Hello")
		self.write(greeting + ", friendly user")
#自定义错误页面/返回内容
	def write_error(self, status_code, **kwargs):
		self.write("Gosh darnit, user! You caused a %d error." % status_code)


if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r'/', IndexHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()