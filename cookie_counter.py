#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop

from tornado.options import define, options
define("port", default=8000, type=int, help="running on the given port")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        cookie = self.get_secure_cookie("count")
        count = int(cookie) + 1 if cookie else 1
        countString = "1 time" if count == 1 else "%d times" % count
        self.write(
            '<html><head><title>Cookie Counter</title></head>' +
            '<body><h1>You’ve viewed this page %s times.</h1>' % countString +
            '</body></html>'
        )
        self.set_secure_cookie("count", str(count))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "debug": True
    }
    app = tornado.web.Application(handlers=[
        (r'/', MainHandler)], **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
