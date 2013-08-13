Introduction
============

PyDic is a set of shell tools (being also python modules) for managing simple
inflectional dictionaries. It uses own dictionary format based on Berkeley DB
and Marisa Trie data structures. Dictionaries can be easily build with provided
tools from raw UTF-8 text files in simple format.

PyDic supports using multiple different dictionaries at the same time.

Preparing a PyDic dictionary
----------------------------

We will focus on example Polish inflectional dictionary. There is an open dictionary
called `SJP <http://sjp.pl/slownik/odmiany/>`_ that can be downloaded and used on variety of licenses (currently GPL, LGPL, CC SA).

Download and unzip SJP dictionary. This will usually produce the file `odm.txt`"::

    $ wget http://sjp.pl/slownik/odmiany/sjp-odm-20130802.zip
    $ unzip sjp-odm-20130802.zip
    $ ls
    README.txt           odm.txt              sjp-odm-20130802.zip

Next step is to convert this file into a format that is PyDic compatible text input (which in that case is just converting file to UTF-8 encoding). For that there is provided very simple shell script::

    $ sjp2pydic odm.txt > sjp.txt


Everything is now ready to create a pydic dictionary for sjp::

    $ pydic_create.py -f sjp.txt

This command will create a dictionary represented by `sjp.pydic` directory.

Quickstart
----------

To test working of simple SJP dictionary just try::

    >>> from pydic import PyDic
    >>> dic = PyDic('sjp.pydic')
    >>> dic.id(u'komputerowi')
    [PyDicId(u'67744@sjp'), PyDicId(u'67748@sjp')]
    >>> dic.id_forms('67744@sjp')
    [u'komputer', u'komputera', u'komputerach', u'komputerami', u'komputerem', u'komputerom', u'komputerowi', u'komputer\xf3w', u'komputery', u'komputerze']

