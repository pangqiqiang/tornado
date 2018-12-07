#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.gen

import json
import urllib
import datetime
import time

from tornado.options import options, define
define("port", default=8000, type=int, help="running on the given port")


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        query = self.get_argument('item')
        headers = {"User-Agent": "iphone7"}
        url = "https://suggest.taobao.com/sug?code=utf-8&q=" + query
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, url, headers=headers)
        body = json.loads(response.body)
        result_count = len(body['result'])
        last_id = body['result'][-1][-1]
        self.write("""
<div style="text-align: center">
<div style="font-size: 72px">%s</div>
<div style="font-size: 144px">%s</div>
<div style="font-size: 24px">Last item id</div>
</div>""" % (result_count, last_id))
        self.finish()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)], debuge=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
