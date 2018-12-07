#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.render('index.html')

    def post(self, *args, **kwargs):
        file_metas = self.request.files["fff"]
        # print(file_metas)
        for meta in file_metas:
            file_name = meta['filename']
            with open(file_name,'wb') as up:
                up.write(meta['body'])

settings = {
    'template_path': 'template',
}

application = tornado.web.Application([
    (r"/index", MainHandler),
], **settings)


if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()