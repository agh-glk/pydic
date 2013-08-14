PyDic - Single dictionary API
=============================

PyDic class is the most low-level API access to the dictionaries. It is responsible for handling single dictionary.

.. autoclass:: pydic.PyDic


Loading dictionary
------------------

PyDic supports both formats. Pre-indexed format of `.pydic` directories which can be generated using `pydic_create.py` shell script or just plain text file. It automatically detects which one was used::

    >>> from pydic import PyDic
    >>> PyDic('sjp.pydic/') # pre-indexed pydic
    >>> PyDic('sjp.txt')    # flat text dictionary

.. note::

    Using pre-indexed PyDic is highly recommended due to indexing overhead. Loading plain text is mainly provided for tests and debug needs.

Word identification namespace
-----------------------------

PyDic internally uses identifiers which are of `PyDicId` type, internally numbered from 1 to total number of words in the dictionary. PyDicId allows you to exactly identify
a given inflectional vector. However  dictionary can also be queried in simplified way, that is without using PyDicId. There is a method naming convention that can help you distinguish which methods are ID-based and which one will simply take any word form (unicode) as an argument. All methods starting with
``word_`` prefix need as an argument a unicode string (a word) and will return also list of unicodes. Other methods starts with ``id_`` prefix means that you will query dictionary using PyDicId.


.. note::

    All methods starting with ``word_`` prefix will return a list in first place. This is because, there can be more than one inflectional vector that can be matched to a given as an argument word form.


.. warning::

    Every single PyDic dictionary uses its own identifiers namespace numbered from 1 with concatenated dictionary name to it separated by `@` sign. This helps to avoid identifies name clashing if you want to use more than one dictionary in your program. Consider also using PyDicManager for managing multiple dictionaries at the same time

Example::

    from pydic import PyDic
    dic = PyDic('sjp.pydic')



``id`` method
-------------

.. automethod:: pydic.PyDic.id

Example::

    >>> dic.id(u'zamkowi')
    [PyDicId(u'187274@sjp'), PyDicId(u'187275@sjp'), PyDicId(u'187358@sjp')]

    >>> dic.id(u'zamek')
    [PyDicId(u'187274@sjp'), PyDicId(u'187275@sjp')]



``id_forms`` method
-------------------
.. automethod:: pydic.PyDic.id_forms

Example::

    >>> dic.id_forms(PyDicId('187274@sjp'))
    [u'zamek', u'zamka', u'zamkach', u'zamkami', u'zamki', u'zamkiem', u'zamkom', u'zamkowi', u'zamk\xf3w', u'zamku']

    >>> dic.id_forms(u'187274@sjp')
    [u'zamek', u'zamka', u'zamkach', u'zamkami', u'zamki', u'zamkiem', u'zamkom', u'zamkowi', u'zamk\xf3w', u'zamku']


``word_forms`` method
---------------------

.. automethod:: pydic.PyDic.word_forms

Example::

    >>> dic.word_forms(u'zamek')
    [[u'zamek', u'zamka', u'zamkach', u'zamkami', u'zamki', u'zamkiem', u'zamkom', u'zamkowi', u'zamk\xf3w', u'zamku'], [u'zamek', u'zamkach', u'zamkami', u'zamki', u'zamkiem', u'zamkom', u'zamkowi', u'zamk\xf3w', u'zamku']]


.. warning::

    As you can see there can be more than one inflectional vector that matches a given word. Therefore this function always
    return list of lists.

.. warning::

    All forms that are used as hash keys are lowercased before used. Forms that are saved in recno are in original case. This means that if you provide form vector like ``IBM:*:IBM:IBMu:IBMowi`` you need to make all queries using lowered case forms like ``ibmowi``, but as a result
    you will get correct vector form ``[u'IBM', u'IBM', u'IBMowi']``. Quering for ``IBMowi`` will return empy result ``[]``.



``id_base`` method
------------------

.. automethod:: pydic.PyDic.id_base

Example::

    >>> dic.id_base('187274@sjp')
    u'zamek'
    >>> dic.id_base(PyDicId(u'187274@sjp'))
    u'zamek'

``word_base`` method
--------------------

.. automethod:: pydic.PyDic.word_base

Example::

    >>> dic.word_base(u'zamkowi')
    [u'zamek', u'zamkowy']



.. warning::

    As you can see there can be more than one inflectional vector that matches a given word. Therefore this function always return list of lists.

.. note::

    Elements on that list are unique, it means that even if there are many lexems found but having the same base form, method will return 1-element list.


``a_id`` method
---------------

.. automethod:: pydic.PyDic.a_id

Example::

    >>> dic.id(u'pszczoly')
    []
    >>> dic.a_id(u'pszczoly')
    [PyDicId(u'134051@sjp'), PyDicId(u'134056@sjp'), PyDicId(u'134050@sjp')]

.. note::

    Default mapping is defined in ``pydic.accents.AccentsTable.PL``

.. warning::

    This method works using ``pydic.Accents`` class which is capable of generating a list of all possible word variants
    using given mapping from standard character to list of accent characters. Be warned that list of possibilities can be
    very long as this is number of combinations from all replaceable characters.

``a_word_forms`` method
-----------------------

.. automethod:: pydic.PyDic.a_word_forms

Example::

    >>> dic.word_forms(u'pszczoly')
    []

    >>> dic.a_word_forms(u'pszczoly')
    [[u'pszczo\u0142a', u'pszczole', u'pszczo\u0142ach', u'pszczo\u0142ami', u'pszczo\u0142\u0105', u'pszczo\u0142\u0119', u'pszczo\u0142o', u'pszczo\u0142om', u'pszczo\u0142y', u'pszcz\xf3\u0142'], [u'pszczo\u0142y', u'pszczo\u0142ach', u'pszczo\u0142ami', u'pszczo\u0142om', u'pszcz\xf3\u0142'], [u'Pszczo\u0142a', u'Pszczole', u'Pszczo\u0142ach', u'Pszczo\u0142ami', u'Pszczo\u0142\u0105', u'Pszczo\u0142\u0119', u'Pszczo\u0142o', u'Pszczo\u0142om', u'Pszczo\u0142owie', u'Pszczo\u0142\xf3w', u'Pszczo\u0142y']]


.. note::

    Default mapping is defined in ``pydic.accents.AccentsTable.PL``

.. warning::

    This method works using ``pydic.Accents`` class which is capable of generating a list of all possible word variants
    using given mapping from standard character to list of accent characters. Be warned that list of possibilities can be
    very long as this is number of combinations from all replaceable characters.

``a_word_base`` method
----------------------

.. automethod:: pydic.PyDic.a_word_base

Example::

    >>> dic.word_base(u'pszczoly')
    []

    >>> dic.a_word_base(u'pszczoly')
    [u'pszczo\u0142a', u'pszczo\u0142y', u'Pszczo\u0142a']


.. note::

    Default mapping is defined in ``pydic.accents.AccentsTable.PL``

.. warning::

    This method works using ``pydic.Accents`` class which is capable of generating a list of all possible word variants
    using given mapping from standard character to list of accent characters. Be warned that list of possibilities can be
    very long as this is number of combinations from all replaceable characters.