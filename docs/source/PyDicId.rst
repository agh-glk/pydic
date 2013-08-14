PyDicId identifiers
===================

PyDicId allows to precisely identify a single dictionary lexem. Identifier is build from two parts:
* sequential number (id property),
* dictionary name (dict property).

Eg.: "123@sjp", "1004@slang-dict", etc.

PyDicId can be created in two simple ways, by constructing PyDic object from str or unicode::

    >>> from pydic import PyDicId
    >>> PyDicId("123@sjp")

or by explicitly defining id and dict properties::

    >>> PyDicId(123, "sjp")

PyDicId are fully interoperable with corresponding strings, so there is a great variety what you can do with that::

    >>> word = PyDicId('123@sjp')
    >>> word == '123@sjp' and word == u'123@sjp'
    True
    >>> word.id
    123
    >>> word.dict
    u'sjp'

In fact whenever PyDicId is required you can also populate string id and it will be automatically converted to corresponding PyDicId.

Having access to PyDicId properties (rather then bare string id) is very convenient for processing multidictionary cases::

    >>> words = [PyDicId(u'123@sjp'), PyDicId(u'124@sjp'), PyDicId(u'123@slang')]
    >>> filter(lambda w: w.dict == 'sjp', words)
    [PyDicId(u'123@sjp'), PyDicId(u'124@sjp')]

.. note::

    Please note that PyDicId are very loosely coupled with dictionaries itself. For example you can easily create some random identifier that does not belong to any dictionary.