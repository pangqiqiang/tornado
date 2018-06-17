#!/usr/bin/env python
#-*-coding:utf-8-*-

import os.path
import tornado.locale
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
from mongohelper import DBHelper

from tornado.options import define, options
define("port", default=8000, type=int, help="run on the given port")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/recommended', RecommendedHandler),
            (r'/edit/([0-9a-zA-Z\-]+)', BookEditHanddler),
            (r'/add', BookEditHanddler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Book": BookModule},
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string("modules/book.html", book=book)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",
                    page_title="Burst's Books!",
                    header_text="Welcome to Burst's Books"
                    )


class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        DB = DBHelper("books")
        books = DB.get_all_books()
        self.render(
            "recommended.html",
            page_title="Burt's Boooks | Recommended Reading",
            header_text="Recommended Reading",
            books=books
        )


class BookEditHanddler(tornado.web.RequestHandler):
    def get(self, isbn=None):
        DB = DBHelper("books")
        book = dict()
        if isbn:
            book = DB.get_book(isbn)
        self.render("book_edit.html",
                    page_title="Burt's Books",
                    header_text="Edit book",
                    book=book)

    def post(self, isbn=None):
        DB = DBHelper("books")
        import time
        book_fields = ['isbn', 'title', 'subtitle', 'image', 'author',
                       'date_released', 'description'
                       ]
        book = dict()
        if isbn:
            book = DB.get_book(isbn)
        for key in book_fields:
            book[key] = self.get_argument(key, None)
        if isbn:
            DB.update_book(isbn, book)
        else:
            book['date_added'] = int(time.time())
            DB.add_book(book)
        self.redirect("/recommended")


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
