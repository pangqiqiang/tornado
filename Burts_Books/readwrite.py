from mongohelper import DBHelper
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import options, define
define("port", default=8000, help="run on the given port", type=int)

DB = DBHelper()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/(\w+)', WordHandler)]
        super().__init__(handlers, debug=True)


class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        word_doc = DB.get(word)
        if word_doc:
            del word_doc["_id"]
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})

    def post(self, word):
        definition = self.get_argument("definition")
        word_doc = DB.get(word)
        if word_doc:
            DB.update(word, definition)
        else:
            DB.add(word, definition)
        res = DB.get(word)
        del res["_id"]
        self.write(res)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
