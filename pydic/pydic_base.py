from bsddb3 import db
import os
from accents import AccentsTable, Accents

from pydic import NAME_FILENAME, FORMS_HASH_FILENAME, FORMS_RECNO_FILENAME

class PyDic(object):
    """
    Abstraction layer for accessing single dictionary
    """

    def __init__(self, dic_path):
        self.dic_path = dic_path
        self.name = open(os.path.join(self.dic_path, NAME_FILENAME)).read().strip()
        self.hash = db.DB()
        self.hash.open(os.path.join(self.dic_path, FORMS_HASH_FILENAME), dbtype=db.DB_HASH)

        self.recno = db.DB()
        self.recno.open(os.path.join(self.dic_path, FORMS_RECNO_FILENAME), dbtype=db.DB_RECNO)
        self.accents = Accents()

    def id(self, word):
        """
        Returns a list of identificators that can be matched for given word form

        :param word: word form
        :type word: unicode
        :return: list of integers or empty list
        """
        try:
            return map( lambda x: int(x), self.hash[word.encode('utf-8')].split(':'))
        except KeyError:
            return []

    def a_id(self, word):
        """
        Accents agnostic version of method ``id()``
        """
        ids = set(self.id(word))
        for w in self.accents.make_accents(word):
            ids.update(self.id(w))
        return list(ids)


    def id_forms(self, id):
        """
        Returns list of forms for a given identificator

        :param id: identificator
        :type id: integer
        :return: list of unicode strings or empty list
        """
        try:
            return self.decode_form(self.recno[id].decode('utf-8'))#[1:]
        except KeyError:
            return []

    def word_forms(self, word):
        """
        Returns list of list of forms for a given word

        :param word: word form
        :type word: unicode
        :return: list of lists of unicode strings or empty list
        """

        return map(lambda x: self.id_forms(x), self.id(word))


    def a_word_forms(self, word, mapping=AccentsTable.PL):
        """
        Accent agnostic version of word_forms method.
        """

        return map(lambda x: self.id_forms(x), self.a_id(word))



    def decode_form(self, string):
        """
        Internal function to decode string format stored in Recno

        :param string:
        :return:
        """
        bits = string.split(':')
        return map(lambda x: bits[0] + x, bits[1:])

    def id_base(self, id):
        """
        Returns a base form of word given as identificator

        :param id: word identificator
        :type id: integer
        :return: unicode string or ``None``
        """
        try:
            return self.decode_form(self.recno[id].decode('utf-8'))[0]
        except KeyError:
            return None

    def word_base(self, word):
        """
        Returns a list of base forms of word

        :param word: word form
        :type word: unicode string
        :return: list of unicode strings or empty list
        """
        return list(set(map(lambda x: self.id_base(x), self.id(word))))


    def a_word_base(self, word):
        """
        Accents agnostic version of ``word_base()`` method
        """
        return list(set(map(lambda x: self.id_base(x), self.a_id(word))))
