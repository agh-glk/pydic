PyDicManager - Multiple dictionary API
======================================

PyDicManager is a class that provides single and clean way to manage multiple dictionaries at the same time.
Constructor method requires paths of all dictionaries that will be used, but after initialisation dictionaries
will be referred by theirs names rather then paths. In fact, dictionary location (path) only matters on loading stage.
Therefore, you can easily move your dictionaries to different place in filesystem as far as you only remember to point
correct path when loading dictionary. Without changing an internal name of a dictionary (which is stored in file ``.pydoc``,
not in a name of a directory) no references of word identificators will be broken.

  .. autoclass:: pydic.PyDicManager

As arguments simple define dictionary paths you want to load.

Word identification namespace
-----------------------------

In difference to PyDic class, PyDicManager provide its own word identification namespace, that is in fact encapsulating
actual PyDic instance identificator (integer) with ``@`` sign and dictionary name.

Format of identificator is: ``<pydic integer identificator>@<pydic name>``

Eg. ``132@first_dictionary``


In this way it is possible to use different words from different dictionaries in one namespace of tokens.

.. warning::

    You should never load dictionaries with the same names, as dictionary name should be unique in program run.

``id`` method
-------------

.. automethod:: pydic.PyDicManager.id

Example::

    >>>> dic.id(u'zamkowi')
    ['123643@gen12', '123644@gen12', '123802@gen12']

    >>>> dic.id(u'zamek')
    ['123643@gen12', '123644@gen12']


``id_forms`` method
-------------------
.. automethod:: pydic.PyDicManager.id_forms

Example::

    >>> dic.id_forms('123643@gen12')
    [u'zamek',
     u'zamka',
     u'zamkowi',
     u'zamek',
     u'zamkiem',
     u'zamku',
     u'zamku',
     u'zamki',
     u'zamk\xf3w',
     u'zamkom',
     u'zamki',
     u'zamkami',
     u'zamkach',
     u'zamki']


``word_forms`` method
---------------------

.. automethod:: pydic.PyDicManager.word_forms

Example::

    >>> dic.word_forms(u'zamek')

    [[u'zamek',
      u'zamka',
      u'zamkowi',
      u'zamek',
      u'zamkiem',
      u'zamku',
      u'zamku',
      u'zamki',
      u'zamk\xf3w',
      u'zamkom',
      u'zamki',
      u'zamkami',
      u'zamkach',
      u'zamki'],
     [u'zamek',
      u'zamek',
      u'zamku',
      u'zamkowi',
      u'zamek',
      u'zamkiem',
      u'zamku',
      u'zamku',
      u'zamki',
      u'zamk\xf3w',
      u'zamkom',
      u'zamki',
      u'zamkami',
      u'zamkach',
      u'zamki']]



.. warning::

    All forms that are used as hash keys are lowercased before used. Forms that are saved in recno are in original case. This means that if you provide form vector like ``IBM:*:IBM:IBMu:IBMowi`` you need to make all queries using lowered case forms like ``ibmowi``, but as a result
    you will get correct vector form ``[u'IBM', u'IBM', u'IBMowi']``. Quering for ``IBMowi`` will return empy result ``[]``.


.. note::

    It is not possible to say which inflectional vector comes from which dictionary, as a returned list is flat. If you need this kind
    of information you will need make query by identificators. This  method assumes that you want to be dictionary agnostic if
    querying by word forms, not by id.

.. warning::

    As you can see there can be more than one inflectional vector that matches a given word. Therefore this function always
    return list of lists. PyDicManager will merge and will make unique all possible vectors from all possible dictionaries.

``id_base`` method
------------------

.. automethod:: pydic.PyDicManager.id_base

Example::

    >>> dic.id_base('123643@gen12')
    u'zamek'

``word_base`` method
--------------------

.. automethod:: pydic.PyDicManager.word_base

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