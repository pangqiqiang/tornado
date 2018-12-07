#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
import tornado.local
import tornado.httpserver
import tornado.options
import tornado.ioloop
import os

from tornado.options import options,define
define("port", default=8000, help="running on the given port", type="int")

class BookModule(tornado.web.UIModule):
	def render(self, book):
		return self.render_string("modules/book.html", book= book)

#	def embedded_javascript(self):
#		return "document.write(\"hi!\")"
#
#	def embedded_css(self):
#		return ".book {background-color:#F5F5F5}"

#	def css_files(self):
#		return "/static/css/newreleases.css"

#	def javascript_files(self):
#		return "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.14/jquery-ui.min.js"


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [(r'/', MainHandler),]
		settings = dict(
		template_path= os.path.join(os.path.dirname(__file__), "templates"),
		static_path= os.path.join(os.path.dirname(__file__), "static"),
		ui_modules = {"Book": BookModule},
		debug= True
		)
		tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("recommended.html",
			page_title="Burt's Books | Recommended Reading",
			header_text="Recommended Reading",
			books=[
					{
					"title":"Programming Collective Intelligence",
					"subtitle": "Building Smart Web 2.0 Applications",
					"image":"/static/images/collective_intelligence.gif",
					"author": "Toby Segaran",
					"date_added":1310248056,
					"date_released": "August 2007",
					"isbn":"978-0-596-52932-1",
					"description":"""<p>This fascinating book demonstrates how you 
					can build web applications to mine the enormous amount of data created by people
					on the Internet. With the sophisticated algorithms in this book, you can write 
					smart programs to access interesting datasets from other web sites, collect data
					from users of your own applications, and analyze and understand the data once
					you've found it.</p>"""
					},
					{
					"title":"RESTful Web Services",
					"subtitle":"Web services for the real world",
					"image": "/static/images/restful_web.gif",
					"author": "Leonard Richardson, Sam Ruby",
					"date_added":1350248056,
					"date_released": "May 2007",
					"isbn":"123-0-596-52932-1",
					"description":"""<p>You've built web sites that can be used by humans
					But can you also build web sites that are usable by machine
					that's where the future lies, this book shows you how to do.</p>"""
					},
					],
				)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	httpserver = tornado.httpserver.HTTPServer(Application())
	httpserver.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

