from bsddb3 import db
import os

from pydic import NAME_FILENAME, FORMS_HASH_FILENAME, FORMS_RECNO_FILENAME

class PyDic(object):
    def __init__(self, dic_path):
        self.dic_path = dic_path
        self.name = open(os.path.join(self.dic_path, NAME_FILENAME)).read().strip()
        self.hash = db.DB()
        self.hash.open(os.path.join(self.dic_path, FORMS_HASH_FILENAME), dbtype=db.DB_HASH)

        self.recno = db.DB()
        self.recno.open(os.path.join(self.dic_path, FORMS_RECNO_FILENAME), dbtype=db.DB_RECNO)

    def word_forms(self, word):
        word = word.encode('utf-8')
        return map(lambda y : self.decode_form(y), map(lambda x: self.recno[x].decode('utf-8'), self.id(word)))

    def id_forms(self, id):
        try:
            return self.decode_form(self.recno[id].decode('utf-8'))
        except KeyError:
            return None

    def decode_form(self, string):
        bits = string.split(':')
        return map(lambda x: bits[0] + x, bits[1:])

    def word_base(self, word):
        forms = self.word_forms(word)
        return map(lambda x: x[0], forms)

    def id_base(self, id):
        forms = self.id_forms(id)
        if forms is None:
            return None
        return self.decode_form(forms)[0]


    def id(self, word):
        try:
            return map( lambda x: int(x), self.hash[word.encode('utf-8')].split(':'))
        except KeyError:
            return []

