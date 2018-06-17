import pymongo
import traceback
import sys
import json

MONGODB_CONFIG = {
    'host': "123.56.21.248",
    'port': 27017,
    'db_name': 'test',
    'username': 'ecloud',
    'password': 'ecloud123',
}


class DBHelper:
    def __init__(self, coll="test"):
        try:
            client = pymongo.MongoClient(
                MONGODB_CONFIG["host"], MONGODB_CONFIG["port"])
            self.db = client[MONGODB_CONFIG["db_name"]]
            if MONGODB_CONFIG["username"] and MONGODB_CONFIG["password"]:
                self.db.authenticate(
                    MONGODB_CONFIG["username"], MONGODB_CONFIG["password"])
            self.coll = self.db[coll]
        except Exception:
            print(traceback.format_exc())
            print('Connect statics Database Failed')
            sys.exit(1)

    def get(self, word):
        res = self.coll.find_one({"word": word})
        return res

    def add(self, word, definition):
        try:
            self.coll.insert({"word": word, "definition": definition})
        except Exception as e:
            print("insert error" + str(e))

    def delete(self, word):
        self.coll.remove({"word": word})

    def update(self, word, definition):
        self.coll.update({"word": word}, {"$set": {"definition": definition}})

    def get_book(self, isbn):
        return self.coll.find_one({"isbn": isbn})

    def get_all_books(self):
        return self.coll.find({})

    def add_book(self, book):
        self.coll.insert(book)

    def update_book(self, isbn, book):
        self.coll.update({"isbn": isbn}, {"$set": book})

    def delete_book(self, isbn):
        self.coll.remove({"isbn": isbn})


if __name__ == "__main__":
    db = DBHelper()
    db.add("perturb", "Bother, unsettle, modify")
    print(db.get("perturb"))
