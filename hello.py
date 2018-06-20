#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop

from tornado.options import define, options
define("port", default=8888, type=int, help="run on the given port")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
<html><body><form method="post" action="/">
<input type="text" name="message">
<input type="submit" value="Submit">
</form></body></html>
			''')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " +
                   self.get_argument("message", ""))


if __name__ == "__main__":
    application = tornado.web.Application(handlers=[
        (r'/', MainHandler)],
        debug=True)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
