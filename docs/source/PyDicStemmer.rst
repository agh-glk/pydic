Stemmer
=======

`Stemming <http://en.wikipedia.org/wiki/Stemming>`_   is the process for reducing inflected (or sometimes derived) words to their stem, base or root form—generally a written word form.

For now stemming module of PyDic allow to index base words from a single dictionary and make an inflection of any word list, building in this way a new dictionaries from new, possibly unknown words.

.. warning::

    Stemmer is currently under heavy development.

Syntax
------
::

    pydic_stemmer.py --help
    usage: pydic_stemmer.py [-h] [-d DELIMITER] -f DICTIONARY_FILE [-t OUTPUT]
                            [-b] [-v]
                            [FILE]

    Makes inflection of a flat text file with words.

    positional arguments:
      FILE                  filename to process

    optional arguments:
      -h, --help            show this help message and exit
      -d DELIMITER, --delimiter DELIMITER
      -f DICTIONARY_FILE, --dictionary-file DICTIONARY_FILE
                            path to file with text dictionary
      -t OUTPUT, --output OUTPUT
                            output file name
      -b, --base-forms      only base forms
      -v, --verbose         debug verbose mode

Input data format
-----------------

A list of base forms of unknown words, eg. ::

    $ cat new.txt
    supermegapojazd
    oktokrążownik


Inflecting words
----------------

::

    $ pydic_stemmer.py -f sjp.pydic new.txt
    supermegapojazd,supermegapojazdach,supermegapojazdami,supermegapojazdem,supermegapojazdom,supermegapojazdowi,supermegapojazdów,supermegapojazdu,supermegapojazdy,supermegapojeździe
    oktokrążownik,oktokrążownika,oktokrążownikach,oktokrążownikami,oktokrążowniki,oktokrążownikiem,oktokrążownikom,oktokrążownikowi,oktokrążowników,oktokrążowniku
