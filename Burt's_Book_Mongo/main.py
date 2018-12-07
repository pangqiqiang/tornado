import os.path
import tornado.locale
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import pymongo

from tornado.options import options, define
define("port", default=8000, type=int, help="running on the given port")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/', MainHandler),
                    (r'/recommended', RecommendedHandler),
                    (r'/add', BookEditHandler),
                    (r'/edit/([0-9Xx\-]*)', BookEditHandler), ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Book": BookModule},
            debug=True,
        )
        conn = pymongo.MongoClient("123.56.21.248", 27017)
        self.db = conn.test
        self.db.authenticate("ecloud", "ecloud123")
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",
                    page_title="Burt's Books | Home",
                    header_text="Welcome to Burt's Books!")


class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.db.books
        books = coll.find()
        self.render("recommended.html",
                    page_title="Burt's Books | Recommended Reading",
                    header_text="Recommended Reading",
                    books=books)


class BookEditHandler(tornado.web.RequestHandler):
    def get(self, isbn=None):
        book = dict()
        if isbn:
            coll = self.application.db.books
            book = coll.find_one({"isbn": isbn}) or dict(isbn=isbn)
        self.render("book_edit.html",
                    page_title="Burt's Books",
                    header_text="Edit book",
                    book=book)

    def post(self, isbn=None):
        import time
        book_fields = ['isbn', 'title', 'subtitle', 'image',
                       'author', 'date_released', 'description']
        coll = self.application.db.books
        book = dict()
        if isbn:
            book = coll.find_one({"isbn": isbn}) or dict(isbn=isbn)
        for key in book_fields:
            book[key] = self.get_argument(key, None)
        if isbn:
            coll.save(book)
        else:
            book['date_added'] = int(time.time())
            coll.insert(book)
        self.redirect("/recommended")


class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string("modules/book.html",
                                  book=book)

    def css_files(self):
        return "/static/css/recommonded.css"

    def javascript_files(self):
        return "/static/js/recommonded.js"


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
