Preparing dictionaries
======================

In order to use PyDic you will need an inflectional dictionary in PyDic's own format. You can easily create one using
provided unix tool named ``pydic_create.py``.

Syntax
------

::

    $ pydic_create.py -h
      usage: pydic_create.py [-h] [-d DICTIONARY_FILE] [-t TARGET] [-n NAME]

      Generate dictionary from text input.

      optional arguments:
        -h, --help            show this help message and exit
        -d DICTIONARY_FILE, --dictionary-file DICTIONARY_FILE
                              path to file with text dictionary
        -t TARGET, --target TARGET
                              path to target dictionary directory
        -n NAME, --name NAME  name of newly created dictionary (default same as text
                              file)

Input
-----
Program takes as an input a file (or if not given with ``-d`` option ``stdin`` will be used) with plain text format ``UTF-8`` dictionary
description.

Format of input is very simple and assumes that in each line there is one word with full inflectional vector::

    <base form>:<grammatical label>:<form 1>:<form 2>:<form 3>: ... :<form n>:

.. note::

    Please note that in current version ``<grammatical label>`` is not used.


.. warning::

    ``<form 1>`` always refers as ``<base form>`` as this is the first form in inflectional vector. In fact ``<base form>`` from the source file is never used in the dictionary itself. This can be used for some additional description of form vector.

You can omit giving dictionary name if you ise ``-d`` argument. Name will be taken by default from dictionary filename (without ``.txt`` or ``.text``) extension. When you do not provide ``-d`` argument, and feed data from ``stdin`` argument ``-n`` is obligatory.

Output
------

Program produces files into specified by argument ``-t`` (``--target``) directory:
 * ``.pydic`` -- this file is a flag that this is a PyDic dictionary folder. At the same time it stores dictionary name which then is used to identify dictionary and as a part of global word identificator used by PyDicManager.


 * ``forms.hash`` -- this file stores DB Berkeley Hash, which have mappings ``"word form"`` ``->`` ``"<id 1>:<id 2>:...<id 3>"``


 * ``forms.recno`` -- this file stores DB Berkeley Recno, which stores following mapping: ``id`` ``->`` ``"<prefix>:<suffix of form 1>:<suffix of form 2>: ... :<suffix of form n>"``


.. warning::

    All forms that are used as hash keys are lowercased before used. Forms that are saved in recno are in original case. This means that if you provide form vector like ``IBM:*:IBM:IBMu:IBMowi`` you need to make all queries using lowered case forms like ``ibmowi``, but as a result
    you will get correct vector form ``[u'IBM', u'IBM', u'IBMowi']``. Quering for ``IBMowi`` will return empy result ``[]``.

.. note::

    If argument ``-t`` (``--target``) is omitted, current directory will be used.

.. note::

    You are supposed never have to touch this internal data structures. This information is given only for your convenience.



Afterwords
----------

Target directory will be created with all required subdirectories if needed. Program will refuse to create dictionary if
in specified target directory there are any of three mentioned above files::

    $ pydic_create.py -d /Users/cypreess/Documents/gen12/gonic.txt -t /Users/cypreess/python_data/dic/gonic/
    Generating gonic dictionary
    !!!Configuration Error: Cowardly refusing to create dictionary in non empty directory


You can move dictionary directory freely and also you can edit name of dictionary in ``.pydic`` file if needed (for example
to create a branch copy). Because you will use this dictionary always referring to its filesystem location you need to only rememeber
path to the dictionary.


Example
-------
Here is an example of creating very small (only 16 words) dictionary::

    $ cat /Users/cypreess/Documents/gen12/gonic.txt
    dogonić : 	BBCA:dogonić:dogonię:dogonisz:dogoni:dogonimy:dogonicie:dogonią:dogoń:##:dogońmy:dogońcie:##:dogoniąc:dogoniący:dogoniłem:dogoniłeś:dogonił:dogoniłam:dogoniłaś:dogoniła:dogoniłom:dogoniłoś:dogoniło:dogoniliśmy:dogoniliście:dogonili:dogoniłyśmy:dogoniłyście:dogoniły:dogoniłbym:dogoniłbyś:dogoniłby:dogoniłabym:dogoniłabyś:dogoniłaby:dogoniłobym:dogoniłobyś:dogoniłoby:dogonilibyśmy:dogonilibyście:dogoniliby:dogoniłybyśmy:dogoniłybyście:dogoniłyby:dogoniono:dogoniony:dogoniwszy:
    gonić : 	BBCA:gonić:gonię:gonisz:goni:gonimy:gonicie:gonią:goń:##:gońmy:gońcie:##:goniąc:goniący:goniłem:goniłeś:gonił:goniłam:goniłaś:goniła:goniłom:goniłoś:goniło:goniliśmy:goniliście:gonili:goniłyśmy:goniłyście:goniły:goniłbym:goniłbyś:goniłby:goniłabym:goniłabyś:goniłaby:goniłobym:goniłobyś:goniłoby:gonilibyśmy:gonilibyście:goniliby:goniłybyśmy:goniłybyście:goniłyby:goniono:goniony:goniwszy:
    gonić się : 	BBCA:gonić się:gonię się:gonisz się:goni się:gonimy się:gonicie się:gonią się:goń się:## się:gońmy się:gońcie się:## się:goniąc się:goniący się:goniłem się:goniłeś się:gonił się:goniłam się:goniłaś się:goniła się:goniłom się:goniłoś się:goniło się:goniliśmy się:goniliście się:gonili się:goniłyśmy się:goniłyście się:goniły się:goniłbym się:goniłbyś się:goniłby się:goniłabym się:goniłabyś się:goniłaby się:goniłobym się:goniłobyś się:goniłoby się:gonilibyśmy się:gonilibyście się:goniliby się:goniłybyśmy się:goniłybyście się:goniłyby się:goniono się:goniony się:goniwszy się:
    nadgonić : 	BBCA:nadgonić:nadgonię:nadgonisz:nadgoni:nadgonimy:nadgonicie:nadgonią:nadgoń:##:nadgońmy:nadgońcie:##:nadgoniąc:nadgoniący:nadgoniłem:nadgoniłeś:nadgonił:nadgoniłam:nadgoniłaś:nadgoniła:nadgoniłom:nadgoniłoś:nadgoniło:nadgoniliśmy:nadgoniliście:nadgonili:nadgoniłyśmy:nadgoniłyście:nadgoniły:nadgoniłbym:nadgoniłbyś:nadgoniłby:nadgoniłabym:nadgoniłabyś:nadgoniłaby:nadgoniłobym:nadgoniłobyś:nadgoniłoby:nadgonilibyśmy:nadgonilibyście:nadgoniliby:nadgoniłybyśmy:nadgoniłybyście:nadgoniłyby:nadgoniono:nadgoniony:nadgoniwszy:
    nagonić : 	BBCA:nagonić:nagonię:nagonisz:nagoni:nagonimy:nagonicie:nagonią:nagoń:##:nagońmy:nagońcie:##:nagoniąc:nagoniący:nagoniłem:nagoniłeś:nagonił:nagoniłam:nagoniłaś:nagoniła:nagoniłom:nagoniłoś:nagoniło:nagoniliśmy:nagoniliście:nagonili:nagoniłyśmy:nagoniłyście:nagoniły:nagoniłbym:nagoniłbyś:nagoniłby:nagoniłabym:nagoniłabyś:nagoniłaby:nagoniłobym:nagoniłobyś:nagoniłoby:nagonilibyśmy:nagonilibyście:nagoniliby:nagoniłybyśmy:nagoniłybyście:nagoniłyby:nagoniono:nagoniony:nagoniwszy:
    odgonić : 	BBCA:odgonić:odgonię:odgonisz:odgoni:odgonimy:odgonicie:odgonią:odgoń:##:odgońmy:odgońcie:##:odgoniąc:odgoniący:odgoniłem:odgoniłeś:odgonił:odgoniłam:odgoniłaś:odgoniła:odgoniłom:odgoniłoś:odgoniło:odgoniliśmy:odgoniliście:odgonili:odgoniłyśmy:odgoniłyście:odgoniły:odgoniłbym:odgoniłbyś:odgoniłby:odgoniłabym:odgoniłabyś:odgoniłaby:odgoniłobym:odgoniłobyś:odgoniłoby:odgonilibyśmy:odgonilibyście:odgoniliby:odgoniłybyśmy:odgoniłybyście:odgoniłyby:odgoniono:odgoniony:odgoniwszy:
    podgonić : 	BBCA:podgonić:podgonię:podgonisz:podgoni:podgonimy:podgonicie:podgonią:podgoń:##:podgońmy:podgońcie:##:podgoniąc:podgoniący:podgoniłem:podgoniłeś:podgonił:podgoniłam:podgoniłaś:podgoniła:podgoniłom:podgoniłoś:podgoniło:podgoniliśmy:podgoniliście:podgonili:podgoniłyśmy:podgoniłyście:podgoniły:podgoniłbym:podgoniłbyś:podgoniłby:podgoniłabym:podgoniłabyś:podgoniłaby:podgoniłobym:podgoniłobyś:podgoniłoby:podgonilibyśmy:podgonilibyście:podgoniliby:podgoniłybyśmy:podgoniłybyście:podgoniłyby:podgoniono:podgoniony:podgoniwszy:
    pogonić : 	BBCA:pogonić:pogonię:pogonisz:pogoni:pogonimy:pogonicie:pogonią:pogoń:##:pogońmy:pogońcie:##:pogoniąc:pogoniący:pogoniłem:pogoniłeś:pogonił:pogoniłam:pogoniłaś:pogoniła:pogoniłom:pogoniłoś:pogoniło:pogoniliśmy:pogoniliście:pogonili:pogoniłyśmy:pogoniłyście:pogoniły:pogoniłbym:pogoniłbyś:pogoniłby:pogoniłabym:pogoniłabyś:pogoniłaby:pogoniłobym:pogoniłobyś:pogoniłoby:pogonilibyśmy:pogonilibyście:pogoniliby:pogoniłybyśmy:pogoniłybyście:pogoniłyby:pogoniono:pogoniony:pogoniwszy:
    przegonić : 	BBCA:przegonić:przegonię:przegonisz:przegoni:przegonimy:przegonicie:przegonią:przegoń:##:przegońmy:przegońcie:##:przegoniąc:przegoniący:przegoniłem:przegoniłeś:przegonił:przegoniłam:przegoniłaś:przegoniła:przegoniłom:przegoniłoś:przegoniło:przegoniliśmy:przegoniliście:przegonili:przegoniłyśmy:przegoniłyście:przegoniły:przegoniłbym:przegoniłbyś:przegoniłby:przegoniłabym:przegoniłabyś:przegoniłaby:przegoniłobym:przegoniłobyś:przegoniłoby:przegonilibyśmy:przegonilibyście:przegoniliby:przegoniłybyśmy:przegoniłybyście:przegoniłyby:przegoniono:przegoniony:przegoniwszy:
    przygonić : 	BBCA:przygonić:przygonię:przygonisz:przygoni:przygonimy:przygonicie:przygonią:przygoń:##:przygońmy:przygońcie:##:przygoniąc:przygoniący:przygoniłem:przygoniłeś:przygonił:przygoniłam:przygoniłaś:przygoniła:przygoniłom:przygoniłoś:przygoniło:przygoniliśmy:przygoniliście:przygonili:przygoniłyśmy:przygoniłyście:przygoniły:przygoniłbym:przygoniłbyś:przygoniłby:przygoniłabym:przygoniłabyś:przygoniłaby:przygoniłobym:przygoniłobyś:przygoniłoby:przygonilibyśmy:przygonilibyście:przygoniliby:przygoniłybyśmy:przygoniłybyście:przygoniłyby:przygoniono:przygoniony:przygoniwszy:
    rozgonić : 	BBCA:rozgonić:rozgonię:rozgonisz:rozgoni:rozgonimy:rozgonicie:rozgonią:rozgoń:##:rozgońmy:rozgońcie:##:rozgoniąc:rozgoniący:rozgoniłem:rozgoniłeś:rozgonił:rozgoniłam:rozgoniłaś:rozgoniła:rozgoniłom:rozgoniłoś:rozgoniło:rozgoniliśmy:rozgoniliście:rozgonili:rozgoniłyśmy:rozgoniłyście:rozgoniły:rozgoniłbym:rozgoniłbyś:rozgoniłby:rozgoniłabym:rozgoniłabyś:rozgoniłaby:rozgoniłobym:rozgoniłobyś:rozgoniłoby:rozgonilibyśmy:rozgonilibyście:rozgoniliby:rozgoniłybyśmy:rozgoniłybyście:rozgoniłyby:rozgoniono:rozgoniony:rozgoniwszy:
    wgonić : 	BBCA:wgonić:wgonię:wgonisz:wgoni:wgonimy:wgonicie:wgonią:wgoń:##:wgońmy:wgońcie:##:wgoniąc:wgoniący:wgoniłem:wgoniłeś:wgonił:wgoniłam:wgoniłaś:wgoniła:wgoniłom:wgoniłoś:wgoniło:wgoniliśmy:wgoniliście:wgonili:wgoniłyśmy:wgoniłyście:wgoniły:wgoniłbym:wgoniłbyś:wgoniłby:wgoniłabym:wgoniłabyś:wgoniłaby:wgoniłobym:wgoniłobyś:wgoniłoby:wgonilibyśmy:wgonilibyście:wgoniliby:wgoniłybyśmy:wgoniłybyście:wgoniłyby:wgoniono:wgoniony:wgoniwszy:
    wygonić : 	BBCA:wygonić:wygonię:wygonisz:wygoni:wygonimy:wygonicie:wygonią:wygoń:##:wygońmy:wygońcie:##:wygoniąc:wygoniący:wygoniłem:wygoniłeś:wygonił:wygoniłam:wygoniłaś:wygoniła:wygoniłom:wygoniłoś:wygoniło:wygoniliśmy:wygoniliście:wygonili:wygoniłyśmy:wygoniłyście:wygoniły:wygoniłbym:wygoniłbyś:wygoniłby:wygoniłabym:wygoniłabyś:wygoniłaby:wygoniłobym:wygoniłobyś:wygoniłoby:wygonilibyśmy:wygonilibyście:wygoniliby:wygoniłybyśmy:wygoniłybyście:wygoniłyby:wygoniono:wygoniony:wygoniwszy:
    zagonić : 	BBCA:zagonić:zagonię:zagonisz:zagoni:zagonimy:zagonicie:zagonią:zagoń:##:zagońmy:zagońcie:##:zagoniąc:zagoniący:zagoniłem:zagoniłeś:zagonił:zagoniłam:zagoniłaś:zagoniła:zagoniłom:zagoniłoś:zagoniło:zagoniliśmy:zagoniliście:zagonili:zagoniłyśmy:zagoniłyście:zagoniły:zagoniłbym:zagoniłbyś:zagoniłby:zagoniłabym:zagoniłabyś:zagoniłaby:zagoniłobym:zagoniłobyś:zagoniłoby:zagonilibyśmy:zagonilibyście:zagoniliby:zagoniłybyśmy:zagoniłybyście:zagoniłyby:zagoniono:zagoniony:zagoniwszy:
    zgonić : 	BBCA:zgonić:zgonię:zgonisz:zgoni:zgonimy:zgonicie:zgonią:zgoń:##:zgońmy:zgońcie:##:zgoniąc:zgoniący:zgoniłem:zgoniłeś:zgonił:zgoniłam:zgoniłaś:zgoniła:zgoniłom:zgoniłoś:zgoniło:zgoniliśmy:zgoniliście:zgonili:zgoniłyśmy:zgoniłyście:zgoniły:zgoniłbym:zgoniłbyś:zgoniłby:zgoniłabym:zgoniłabyś:zgoniłaby:zgoniłobym:zgoniłobyś:zgoniłoby:zgonilibyśmy:zgonilibyście:zgoniliby:zgoniłybyśmy:zgoniłybyście:zgoniłyby:zgoniono:zgoniony:zgoniwszy:
    zgonić się : 	BBCA:zgonić się:zgonię się:zgonisz się:zgoni się:zgonimy się:zgonicie się:zgonią się:zgoń się:## się:zgońmy się:zgońcie się:## się:zgoniąc się:zgoniący się:zgoniłem się:zgoniłeś się:zgonił się:zgoniłam się:zgoniłaś się:zgoniła się:zgoniłom się:zgoniłoś się:zgoniło się:zgoniliśmy się:zgoniliście się:zgonili się:zgoniłyśmy się:zgoniłyście się:zgoniły się:zgoniłbym się:zgoniłbyś się:zgoniłby się:zgoniłabym się:zgoniłabyś się:zgoniłaby się:zgoniłobym się:zgoniłobyś się:zgoniłoby się:zgonilibyśmy się:zgonilibyście się:zgoniliby się:zgoniłybyśmy się:zgoniłybyście się:zgoniłyby się:zgoniono się:zgoniony się:zgoniwszy się:

    $ pydic_create.py -d /Users/cypreess/Documents/gen12/gonic.txt -t /Users/cypreess/python_data/dic/gonic2/
    Generating gonic dictionary
    [ 1 ] dogonić
    [ 2 ] gonić
    [ 3 ] gonić się
    [ 4 ] nadgonić
    [ 5 ] nagonić
    [ 6 ] odgonić
    [ 7 ] podgonić
    [ 8 ] pogonić
    [ 9 ] przegonić
    [ 10 ] przygonić
    [ 11 ] rozgonić
    [ 12 ] wgonić
    [ 13 ] wygonić
    [ 14 ] zagonić
    [ 15 ] zgonić
    [ 16 ] zgonić się


You can also run this command using ``stdin``::

    $ cat /Users/cypreess/Documents/gen12/gonic.txt | pydic_create.py  -t /Users/cypreess/python_data/dic/gonic2/ -n gonic
    Generating gonic dictionary
    [ 1 ] dogonić
    [ 2 ] gonić
    [ 3 ] gonić się
    [ 4 ] nadgonić
    [ 5 ] nagonić
    [ 6 ] odgonić
    [ 7 ] podgonić
    [ 8 ] pogonić
    [ 9 ] przegonić
    [ 10 ] przygonić
    [ 11 ] rozgonić
    [ 12 ] wgonić
    [ 13 ] wygonić
    [ 14 ] zagonić
    [ 15 ] zgonić
    [ 16 ] zgonić się


.. warning::

    Remember to use ``-n`` option to give a name for a dictionary when using ``stdin`` input.