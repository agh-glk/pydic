PyDic - Single dictionary API
=============================

PyDic class is the most low-level API access to the dictionaries. It is responsible for reading a single path with PyDic format dictionary.

.. autoclass:: pydic.PyDic

Word identification namespace
-----------------------------

PyDic internally uses identificators (which are of `PyDicId` type, numbered from 1 to total number of words). If you need to exactly identify
a given inflectional vector this is what you need to use. However  dictionary can also be queried in simplified way, that is without using those internal identificators. There is a method naming convention that can help you distinguish which metods are ID-based and which one will simply take any word form (unicode) as an argument. All methods starting with
``word_`` prefix need as an argument a unicode string (a word) and will return also list of unicodes. Other methods starts with ``id_`` prefix means that you will query dictionary using internal identificator.


.. note::

    All methods starting with ``word_`` prefix will return a list in first place. This is because, there can be more than one inflectional vector that can be matched to a given as an argument word form.


.. warning::

    Every single PyDic dictionary uses its own identificator namespace numbered from 1 with concatenated dictionary name to it separated by `@` sign. This helps to avoid identificator name clashing if you want to use more than one dictionary in your program. Consider also using PyDicManager for managing multiple dictionaries at the same time

Example::

    from pydic import PyDic
    dic = PyDic('/Users/cypreess/python_data/dic/gen12/')



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

    >>> dic.id_base(123643)
    u'zamek'

``word_base`` method
--------------------

.. automethod:: pydic.PyDic.word_base

Example::

    >>> dic.word_base(u'zamkowi')
    [u'zamek', u'zamkowy']



.. warning::

    All forms that are used as hash keys are lowercased before used. Forms that are saved in recno are in original case. This means that if you provide form vector like ``IBM:*:IBM:IBMu:IBMowi`` you need to make all queries using lowered case forms like ``ibmowi``, but as a result
    you will get correct vector form ``[u'IBM', u'IBM', u'IBMowi']``. Quering for ``IBMowi`` will return empy result ``[]``.


.. warning::

    As you can see there can be more than one inflectional vector that matches a given word. Therefore this function always
    return list of lists.

.. note::

    Elements on that list are unique.


``a_id`` method
---------------

.. automethod:: pydic.PyDic.a_id

Example::

    >>> dic.id(u'pszczoly')
    []
    
    >>> dic.a_id(u'pszczoly')
    [81898]

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
    [[u'pszczo\u0142a', u'pszczo\u0142y', u'pszczole', u'pszczo\u0142\u0119', u'pszczo\u0142\u0105', u'pszczole', u'pszczo\u0142o', u'pszczo\u0142y', u'pszcz\xf3\u0142', u'pszczo\u0142om', u'pszczo\u0142y', u'pszczo\u0142ami', u'pszczo\u0142ach', u'pszczo\u0142y']]


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
    [u'pszczo\u0142a']


.. note::

    Default mapping is defined in ``pydic.accents.AccentsTable.PL``

.. warning::

    This method works using ``pydic.Accents`` class which is capable of generating a list of all possible word variants
    using given mapping from standard character to list of accent characters. Be warned that list of possibilities can be
    very long as this is number of combinations from all replaceable characters.