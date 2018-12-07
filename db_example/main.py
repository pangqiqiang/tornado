import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop
import pymongo


from tornado.options import options, define
define("port",default=8000, type=int, help="running on the given port")

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[(r'/(\w+)', MainHandler)]
        conn = pymongo.MongoClient("123.56.21.248",27017)
        self.db = conn.test
        self.db.authenticate('ecloud', 'ecloud123')
        super(Application, self).__init__(handlers, debug=True)


class MainHandler(tornado.web.RequestHandler):
    def get(self, word):
        coll = self.application.db.words
        word_doc = coll.find_one({"word": word})
        if word_doc:
            del word_doc["_id"]
            self.write(word_doc)
        else:
            self.set_status(400)
            self.write({"error": "word not found"})

    def post(self, word):
        definition = self.get_argument("definition")
        coll = self.application.db.words
        word_doc = coll.find_one({"word": word})
        if word_doc:
            word_doc['definition'] = definition
            coll.save(word_doc)
        else:
            word_doc = {'word': word, 'definition': definition}
            coll.insert(word_doc)
        del word_doc["_id"]
        self.write(word_doc)

if __name__ == "__main__":
    options.parse_command_line()
    httpserver = tornado.httpserver.HTTPServer(Application())
    httpserver.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()