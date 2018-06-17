import os.path
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop

from tornado.options import define, options
define("port", default=8000, type=int, help="running on the given port")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument("noun1")
        noun2 = self.get_argument("noun2")
        verb = self.get_argument("verb")
        noun3 = self.get_argument("noun3")
        self.render("poem.html", roads=noun1, wood=noun2,
                    made=verb, difference=noun3)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/poem', PoemPageHandler)
        ],
        template_path=os.path.join(
            os.path.dirname(__file__), "templates")
    )
    http = tornado.httpserver.HTTPServer(app)
    http.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
