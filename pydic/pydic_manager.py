import os

from pydic import NAME_FILENAME
from pydic import PyDic

class PyDicManager(object):
    """
    Manages single access to multiple PyDic instances
    """

    def __init__(self, *args):
        self.dictionaries = {}
        for path in args:
            self.load_dictionary(path)


    def get_dictionaries(self):
        return self.dictionaries.keys()

    def load_dictionary(self, path):
        dic = PyDic(path)
        self.dictionaries[dic.name] = dic


    def parse_full_id(self, full_id):
        id, dic = full_id.split('@')
        return (int(id), dic)

    def make_full_id(self, id, dic_name):
        return "%d@%s" % (id, dic_name)

    def id (self, word):
        """
        Returns all known id for a word from every dictionary

        :param word: a word form
        :type word: unicode
        :return: list of str full id
        """
        result = []
        for dic_name in self.dictionaries.keys():
            result += map(lambda x: self.make_full_id(x, dic_name), self.dictionaries[dic_name].id(word))
        return result

    def id_forms(self, full_id):
        """
        Returns forms vector for a full_id

        :param full_id: word full id
        :type full_id: str
        :return: list of unicode forms or empty list
        """
        try:
            id, dic = self.parse_full_id(full_id)
            return self.dictionaries[dic].id_forms(id)
        except (ValueError, KeyError):
                  return None

    def id_base(self, full_id):
        """
        Returns base form for a full id

        :param full_id: word full id
        :type full_id: str
        :return: word base form as unicode or None
        """
        try:
            id, dic = self.parse_full_id(full_id)
            return self.dictionaries[dic].id_base(int(id))
        except (ValueError, KeyError):
            return None


    def word_forms(self, word):
        """
        For a word form returns a list of unique forms vector.

        :param word: a word form
        :type word: unicode
        :return: unique list of vector forms as tuple

        """
        result = set()
        for dic_name in self.dictionaries.keys():
            for vector in self.dictionaries[dic_name].word_forms(word):

                result.add(tuple(vector))
        return filter(lambda x: len(x), result)

    def word_base(self, word):
        """
        Returns unique word base forms for a given word

        :param word: a word form
        :type word: unicode
        :return: unique list of forms as unicode
        """
        return list(set(map(lambda x: self.id_base(x), self.id(word))))