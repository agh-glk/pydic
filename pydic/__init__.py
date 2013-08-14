# -*- coding: utf8 -*-

class ConfigurationErrorException(Exception):
    pass

NAME_FILENAME = '.pydic'
FORMS_HASH_FILENAME = 'forms.hash'
FORMS_RECNO_FILENAME = 'forms.recno'
FORMS_RECNO_INDEX_FILENAME = 'forms.recno.index'


from accents import Accents
from pydic_base import PyDic, PyDicId
from pydic_manager import PyDicManager
from pydic_stemmer import PydicStemmer
from pydic_create import PyDicCreator
