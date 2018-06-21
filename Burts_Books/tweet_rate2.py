#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
import tornado.options
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.gen

import urllib
import json
import time
import datetime

from tornado.options import options, define
define("port", default=8000, type=int, help="run on the given port")


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        type = self.get_argument('type', '1')
        page = self.get_argument('page', '1')
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,
                                          "https://www.apiopen.top/satinApi?" +
                                          urllib.parse.urlencode({"page": page, "type": type}))
        body = json.loads(response.body)
        result_count = len(body['data'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = " ".join(body['data'][-1]['passtime'].split())
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
                                                     "%Y-%m-%d %H:%M:%S")
        secconds_diff = time.mktime(now.timetuple()) - \
            time.mktime(oldest_tweet_at.timetuple())
        tweets_per_second = float(result_count) / secconds_diff
        self.write('''
<div style="text-align: center">
<div style="font-size: 72px">%s</div>
<div style="font-size: 144px">%.05f</div>
<div style="font-size: 24px">tweets per second</div>
</div>''' % (type, tweets_per_second))
        self.finish()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = tornado.web.Application(handlers=[
        (r'/', IndexHandler)],
        debug=True)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
