from collections import OrderedDict
import os
import sys

from bsddb3 import db

from accents import AccentsTable, Accents
from pydic import NAME_FILENAME, FORMS_HASH_FILENAME, FORMS_RECNO_FILENAME, ConfigurationErrorException


class PyDic(object):
    """
    Abstraction layer for accessing single dictionary
    """

    INTERNAL_DELIMITER = ':'

    def __init__(self, path):
        if os.path.isdir(path):
            self.read_pydic_index(path)
        elif os.path.isfile(path):
            self.make_memory_pydic_index(path)
        else:
            raise RuntimeError("Wrong pydic input resource")
        self.accents = Accents()


    def __iter__(self):
        return iter(xrange(1, len(self.recno) + 1))


    def id(self, word):
        """
        Returns a list of identificators that can be matched for given word form

        :param word: word form
        :type word: unicode
        :return: list of integers or empty list
        """
        try:
            return map(lambda x: int(x),
                       self.hash[word.encode('utf-8')].split(PyDic.INTERNAL_DELIMITER))
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
        bits = string.split(PyDic.INTERNAL_DELIMITER)
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


    def read_pydic_index(self, dic_path):
        self.dic_path = dic_path
        self.name = open(
            os.path.join(self.dic_path, NAME_FILENAME)).read().strip()
        self.hash = db.DB()
        self.hash.open(os.path.join(self.dic_path, FORMS_HASH_FILENAME),
                       dbtype=db.DB_HASH)

        self.recno = db.DB()
        self.recno.open(os.path.join(self.dic_path, FORMS_RECNO_FILENAME),
                        dbtype=db.DB_RECNO)


    def make_memory_pydic_index(self, from_source, name=None, delimiter=',',
                                verbose=False):
        self.hash, self.recno = PyDic.make_pydic_index(from_source=open(from_source),
                                                       to_path=None, name=name,
                                                       delimiter=delimiter,
                                                       verbose=verbose)

        self.name = from_source


    @staticmethod
    def make_pydic_index(from_source, to_path, name, delimiter=',', verbose=False):


        if to_path is not None and (
                    os.path.exists(
                            os.path.join(to_path, NAME_FILENAME)) or os.path.exists(
                        os.path.join(to_path, NAME_FILENAME)) or os.path.exists(
                    os.path.join(to_path, NAME_FILENAME))):
            raise ConfigurationErrorException(
                'Cowardly refusing to create dictionary in non empty directory')

        if to_path is not None and not os.path.exists(to_path):
            os.makedirs(to_path)

        if to_path is not None:
            name_file = open(os.path.join(to_path, NAME_FILENAME), 'w')
            name_file.write(name.encode('utf-8') + '\n')
            name_file.close()

        dbhash = db.DB()
        dbrecno = db.DB()
        if to_path is not None:
            dbhash.open(os.path.join(to_path, FORMS_HASH_FILENAME), dbtype=db.DB_HASH,
                        flags=db.DB_CREATE)
            dbrecno.open(os.path.join(to_path, FORMS_RECNO_FILENAME), dbtype=db.DB_RECNO,
                         flags=db.DB_CREATE)
        else:
            dbhash.open(None, dbtype=db.DB_HASH, flags=db.DB_CREATE)
            dbrecno.open(None, dbtype=db.DB_RECNO, flags=db.DB_CREATE)

        for line in from_source:
            bits = line.split(delimiter)
            bits = map(lambda x: x.strip().decode('utf-8'), bits)
            bits = filter(lambda x: x, bits)
            if bits:
                bits = OrderedDict.fromkeys(bits).keys() # stable unique
                bits_prefixed = PyDic.common_prefix(bits)
                wid = dbrecno.append(
                    (PyDic.INTERNAL_DELIMITER.join(bits_prefixed)).encode('utf-8'))
                if verbose:
                    print >> sys.stderr, "[", wid, "]", bits[0]

                for bit in set(bits):
                    form = bit.lower().encode('utf-8')
                    try:
                        dbhash[form] = "%s:%s" % (dbhash[form], str(wid))
                    except KeyError:
                        dbhash[form] = str(wid)

        return dbhash, dbrecno

    @staticmethod
    def common_prefix(word_list):
        """
        For a list of words produces a list of [optimal prefix, suffix1, suffix2...]
        :param word_list:
        :return:
        """
        i = min(map(lambda x: len(x), word_list))
        while i > 0:
            lst = map(lambda x: x[0:i], word_list)
            # http://stackoverflow.com/questions/3844801
            # Fastest checking if lst has the same values
            if (not lst or lst.count(lst[0]) == len(lst)):
                break
            i -= 1
        return [word_list[0][0:i]] + map(lambda x: x[i:], word_list)

