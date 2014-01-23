from pydic import PyDic, PyDicId
from accents import AccentsTable, Accents


def require_valid_pydic_id(method):
    def decorated(self, pydic_id):
        if type(pydic_id) == PyDicId:
            if not self.dictionaries.has_key(pydic_id.dict):
                raise ValueError('PyDic ID from unknown dictionary')
        else:
            pydic_id = PyDicId(pydic_id)
        return method(self, pydic_id)
    decorated.__doc__ = method.__doc__
    decorated.__repr__ = method.__repr__
    return decorated

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

    def id(self, word):
        """
        Returns all known id for a word from every dictionary

        :param word: a word form
        :type word: unicode
        :return: list of str full id
        """
        result = []
        for dic_name in self.dictionaries.keys():
            result += self.dictionaries[dic_name].id(word)
        return result

    @require_valid_pydic_id
    def id_forms(self, pydic_id):
        """
        Returns forms vector for a full_id

        :param pydic_id: word full id
        :type pydic_id: str
        :return: list of unicode forms or empty list
        """
        try:
            return self.dictionaries[pydic_id.dict].id_forms(pydic_id)
        except (ValueError, KeyError):
            return None

    @require_valid_pydic_id
    def id_base(self, pydic_id):
        """
        Returns base form for a full id

        :param pydic_id: word full id
        :type pydic_id: str
        :return: word base form as unicode or None
        """
        try:
            return self.dictionaries[pydic_id.dict].id_base(pydic_id)
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
        
    def a_id(self, word):
        """
        Accents agnostic version of method ``id()``

        :param form: form
        :type form: unicode
        :return: list of PyDicId or empty list
        """
        result = []
        for dic_name in self.dictionaries.keys():
            result += self.dictionaries[dic_name].a_id(word)
        return result
        
    def a_word_forms(self, form, mapping=AccentsTable.PL):
        """
        Accent agnostic version of word_forms method.

        :param form: word form
        :type form: unicode
        :return: list of lists of unicode strings or empty list
        """
        result = set()
        for dic_name in self.dictionaries.keys():
            for vector in self.dictionaries[dic_name].a_word_forms(form):
                result.add(tuple(vector))
        return filter(lambda x: len(x), result)
    
    def a_word_base(self, form):
        """
        Accents agnostic version of ``word_base()`` method

        :param form: word form
        :type form: unicode string
        :return: list of unicode strings or empty list
        """
        return list(set(map(lambda x: self.id_base(x), self.a_id(form))))
        
