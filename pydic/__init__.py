class ConfigurationErrorException(Exception):
    pass

NAME_FILENAME = '.pydic'
FORMS_HASH_FILENAME = 'forms.hash'
FORMS_RECNO_FILENAME = 'forms.recno'


from pydic_base import PyDic
from pydic_manager import PyDicManager