#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop

from tornado.options import options, define
define("port", default=8000, help="running on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        cookie = self.get_secure_cookie("count")
        count = int(cookie) + 1 if cookie else 1

        countString = "1 time" if count == 1 else "%d times" % count
        self.set_secure_cookie("count", str(count))

        self.write(
            '<html><head><title>Cookie Counter</title></head>' +
            '<body><h1>You’ve viewed this page %s times.</h1>' % countString +
            '</body></html>'
        )


if __name__ == "__main__":
    app = tornado.web.Application(
        handlers=[
            (r'/', MainHandler),
        ],
        cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        debuge=True
    )

    httpserver = tornado.httpserver.HTTPServer(app)
    httpserver.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
