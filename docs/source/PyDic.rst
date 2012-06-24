PyDic - Single dictionary API
=============================

PyDic class is the most low-level API access to the dictionaries. It is responsible for reading a single
path with PyDic format dictionary.

.. autoclass:: pydic.PyDic


PyDic internally uses identificators (which are Intgeres numbered from 1 to number of words). If you need to identify
a given inflectional vector this is what you need to use. However querying dictionary can also be used in simplified way, that is without internal identificators. There is a method naming convention that can help you using this API. All methods starting with
``word_`` prefix need as an argument a unicode string (a word) and will return also unicodes. Other methods starts with
``id_`` prefix means that you will query dictionary using internal identificator.

.. warning::

    Every single PyDic dictionary uses its own identificator namespace numbered from 1. If you want to use more than one dictionary in your program you should always use PyDicManager, as it introduces its own identificators namespacing, eg. ``1234@first_dic`` , ``1234@second_dict``. This will help you to avoid identificators clashing.

Example::

    from pydic import PyDic
    dic = PyDic('/Users/cypreess/python_data/dic/gen12/')


``id`` method
-------------

.. automethod:: pydic.PyDic.id

Example::

    >> dic.id(u'zamkowi')
    [123643, 123644, 123802]

    >> dic.id(u'zamek')
    [123643, 123644]


``id_forms`` method
-------------------
.. automethod:: pydic.PyDic.id_forms

Example::

    >> dic.id_forms(123643)
    [u'zamek',
     u'zamek',
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

.. automethod:: pydic.PyDic.word_forms

Example::

    >> dic.word_forms(u'zamek')

    [[u'zamek',
      u'zamek',
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

    As you can see there can be more than one inflectional vector that matches a given word. Therefore this function always
    return list of lists.

``id_base`` method
------------------

.. automethod:: pydic.PyDic.id_base

Example::

    >> dic.id_base(123643)
    u'zamek'

``word_base`` method
--------------------

.. automethod:: pydic.PyDic.word_base

Example::

    >> dic.word_base(u'zamkowi')
    [u'zamek', u'zamek', u'zamkowy']


.. warning::

    As you can see there can be more than one inflectional vector that matches a given word. Therefore this function always
    return list of lists.

.. warning::

    Elements on that list can be NOT unique.