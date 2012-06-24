import os

from pydic import NAME_FILENAME
from pydic import PyDic

class PyDicManager(object):
    """
    Manages single access to multiple PyDic's
    """

    def __init__(self, *args):
        self.dictionaries = {}
        for path in args:
            self.load_dictionary(path)

    def load_dictionary(self, path):
        dic = PyDic(path)
        self.dictionaries[dic.name] = dic

    def id_base(self, id):
        try:
            id, dic = id.split('@')
            return self.dictionaries[dic].id_base(int(id))
        except (ValueError, KeyError):
            return None

    def id (self, word):
        result = []
        for dic in self.dictionaries.keys():
            result += map(lambda x: "%d@%s" % (x, dic), self.dictionaries[dic].id(word))
        return result