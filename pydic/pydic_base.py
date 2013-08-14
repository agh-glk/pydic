from collections import OrderedDict
from itertools import imap
import os
import sys
from bsddb3 import db
from accents import AccentsTable, Accents
from pydic import NAME_FILENAME, FORMS_HASH_FILENAME, FORMS_RECNO_FILENAME, ConfigurationErrorException


class PyDicId(object):
    """
    Dictionary lexem identifier. Build from sequential number (an id) and
    dictionary name concatenated with '@' sign, eg. '123@sjp'
    """
    SEPARATOR = '@'

    def __init__(self, ident=None, dict_name=None):
        if (type(ident) == str or type(ident) == unicode) and dict_name is None:
            self.id, self.dict = self.parse_text_ident(ident)
        elif ident is not None and dict_name is not None:
            self.id = int(ident)
            self.dict = unicode(dict_name)
        else:
            raise ValueError('Cannot create valid PyDic ID')

    def parse_text_ident(self, text_ident):
        ident, dictionary = unicode(text_ident).split(PyDicId.SEPARATOR)
        return (int(ident), dictionary)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(unicode(self)))

    def __str__(self):
        return "%d%s%s" % (self.id, PyDicId.SEPARATOR, self.dict)

    def __unicode__(self):
        return u"%d%s%s" % (self.id, PyDicId.SEPARATOR, self.dict)

    def __eq__(self, other):
        if type(other) == self.__class__:
            return self.dict == other.dict and self.id == other.id
        elif type(other) == str or type(other) == unicode:
            other = PyDicId(other)
            return self.dict == other.dict and self.id == other.id
        else:
            raise NotImplemented()

    def __hash__(self):
        return hash(unicode(self))


def require_valid_pydic_id(method):
    # do something that requires view's class
    def decorated(self, pydic_id):
        if type(pydic_id) == PyDicId:
            if not pydic_id.dict == self.name:
                raise ValueError('PyDic ID from different dictionary')
        elif type(pydic_id) in (str, unicode):
            pydic_id = PyDicId(pydic_id)
        elif type(pydic_id) == int:
            pydic_id = PyDicId(pydic_id, self.name)
        else:
            pydic_id = PyDicId(pydic_id)
        return method(self, pydic_id)

    decorated.__doc__ = method.__doc__
    decorated.__repr__ = method.__repr__
    return decorated


class PyDic(object):
    """
    Abstraction layer for accessing single dictionary
    """
    DIR_EXTENSION = 'pydic'
    INTERNAL_DELIMITER = ':'

    def __init__(self, path):
        self.path = path
        if os.path.isdir(self.get_path()):
            self.read_pydic_index(self.get_path())
        elif os.path.isfile(self.path):
            self.make_memory_pydic_index(self.get_path())
        else:
            raise RuntimeError("Wrong pydic input resource")
        self.accents = Accents()


    def __iter__(self):
        return imap(lambda i: PyDicId(i, self.name), xrange(1, len(self.recno) + 1))

    def is_inmemory(self):
        """
        Checks if dictionary is in in-memory only mode. It is needed by other modules
        willing to write some intermediate file structures to pydic folder.
        """
        return os.path.isfile(self.path)

    def get_path(self, join_with=None):

        if join_with:
            return os.path.join(self.path, join_with)
        else:
            return self.path

    def id(self, form):
        """
        Returns a list of PyDicId that match a given word form

        :param form: word form
        :type form: unicode
        :return: list of PyDicId or empty list
        """
        try:
            return map(lambda x: PyDicId(int(x), self.name),
                       self.hash[form.lower().encode('utf-8')].split(
                           PyDic.INTERNAL_DELIMITER))
        except KeyError:
            return []

    def a_id(self, form):
        """
        Accents agnostic version of method ``id()``

        :param form: form
        :type form: unicode
        :return: list of PyDicId or empty list
        """
        ids = set(self.id(form))
        for w in self.accents.make_accents(form.lower()):
            ids.update(self.id(w))
        return list(ids)

    @require_valid_pydic_id
    def id_forms(self, pydic_id):
        """
        Returns list of forms for a given PyDicId

        :param pydic_id: PyDicId or string id
        :type pydic_id: PyDicId, string
        :return: list of unicode strings or empty list
        """
        try:
            return self.__decode_form(self.recno[pydic_id.id].decode('utf-8'))
        except KeyError:
            return []

    def word_forms(self, form):
        """
        Returns list of list of forms for a given form

        :param form: word form
        :type form: unicode
        :return: list of lists of unicode strings or empty list
        """

        return map(lambda x: self.id_forms(x), self.id(form))


    def a_word_forms(self, form, mapping=AccentsTable.PL):
        """
        Accent agnostic version of word_forms method.

        :param form: word form
        :type form: unicode
        :return: list of lists of unicode strings or empty list
        """

        return map(lambda x: self.id_forms(x), self.a_id(form))


    def __decode_form(self, string):
        """
        Internal function to decode string format stored in Recno

        :param string:
        :return:
        """
        bits = string.split(PyDic.INTERNAL_DELIMITER)
        return map(lambda x: bits[0] + x, bits[1:])

    @require_valid_pydic_id
    def id_base(self, pydic_id):
        """
        Returns a base form of word given as PyDicId

        :param pydic_id: PyDicId
        :type pydic_id: PyDicId, string
        :return: unicode string or ``None``
        """

        try:
            return self.__decode_form(self.recno[pydic_id.id].decode('utf-8'))[0]
        except KeyError:
            return None

    def word_base(self, form):
        """
        Returns a list of base forms of form

        :param form: word form
        :type form: unicode string
        :return: list of unicode strings or empty list
        """
        return list(set(map(lambda x: self.id_base(x), self.id(form))))


    def a_word_base(self, form):
        """
        Accents agnostic version of ``word_base()`` method

        :param form: word form
        :type form: unicode string
        :return: list of unicode strings or empty list
        """
        return list(set(map(lambda x: self.id_base(x), self.a_id(form))))


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
                                                       to_path=None,
                                                       name=name,
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

