Preparing dictionaries
======================

To speed things up every dictionary you are going to use should be indexed first. You can easily create one using provided unix tool named ``pydic_create.py``. After creating and index from flat text file technically you don't need it any more.

Syntax
------

::

    $ pydic_create.py --help
    usage: pydic_create.py [-h] [-d DELIMITER] [-f DICTIONARY_FILE] [-t TARGET]
                           [-n NAME] [-v]

    Generate dictionary from text input.

    optional arguments:
      -h, --help            show this help message and exit
      -d DELIMITER, --delimiter DELIMITER
                            delimiter
      -f DICTIONARY_FILE, --dictionary-file DICTIONARY_FILE
                            path to file with text dictionary
      -t TARGET, --target TARGET
                            path to target dictionary directory
      -n NAME, --name NAME  name of newly created dictionary (default same as text
                            file)
      -v, --verbose


Input format
------------

Program takes as an input a file (or if not given with ``-f`` option ``stdin`` will be used) with plain text format ``UTF-8`` dictionary description.

Format of input is very simple and assumes that in each line there is one word with full inflectional vector::

    <base form | form 1>:<form 2>:<form 3>: ... :<form n>


.. warning::

    ``<form 1>`` always refers as ``<base form>`` as this is the first form in inflectional vector.


You can omit giving dictionary name if you use ``-f`` argument. Name will be taken by default from dictionary filename (extracting ``.txt`` or ``.text`` extension). When you do not provide ``-f`` argument and feed data from ``stdin``  providing at least ``-n`` argument is obligatory.

Output
------

Program produces files into specified by argument ``-t`` (``--target``) directory. The files are being generated are:
 * ``.pydic`` -- this file is a flag that this is a PyDic dictionary folder. At the same time it stores dictionary name which then is used to identify dictionary and as a part of global word identificator used by PyDicManager.
 * ``forms.hash`` -- this file stores DB Berkeley Hash, which have mappings ``"word form"`` ``->`` ``"<id 1>:<id 2>:...<id 3>"``
 * ``forms.recno`` -- this file stores DB Berkeley Recno, which stores following mapping: ``id`` ``->`` ``"<prefix>:<suffix of form 1>:<suffix of form 2>: ... :<suffix of form n>"``


.. note::

    All forms that are used as hash keys (index search) are lowercased before saved. Forms that are saved in recno are in original case. This means that if you provide form vector like ``IBM:*:IBM:IBMu:IBMowi`` you will get this vector both queering  forms like `ibmowi` and `IBMOWI`.

.. note::

    If argument ``-t`` (``--target``) is omitted current directory will be used.

.. warning::

    You are supposed never have to touch this internal data structures. This information is given only for your convenience.



Afterwords
----------

Target directory will be created with all required subdirectories if needed. Program will refuse to create dictionary if
in specified target directory there are any of three mentioned above files::

    $ pydic_create.py -f sjp.txt  -t sjp
    Generating sjp dictionary
    !!!Configuration Error: Cowardly refusing to create dictionary in non empty directory


You can move dictionary directory freely and also you can edit name of dictionary in ``.pydic`` file if needed (for example
to create a branch). Because you will use this dictionary always referring to its filesystem location you need to only remember path to the dictionary.


Example
-------
Here is an example of creating very small (only 16 words) dictionary::

    $ cat sjp.10.txt
    ablaktacja, ablaktacjach, ablaktacjami, ablaktacją, ablaktacje, ablaktację, ablaktacji, ablaktacjo, ablaktacjom, ablaktacyj
    ablaktowalny, ablaktowalna, ablaktowalną, ablaktowalne, ablaktowalnego, ablaktowalnej, ablaktowalnemu, ablaktowalni, ablaktowalnych, ablaktowalnym, ablaktowalnymi, nieablaktowalna, nieablaktowalną, nieablaktowalne, nieablaktowalnego, nieablaktowalnej, nieablaktowalnemu, nieablaktowalni, nieablaktowalny, nieablaktowalnych, nieablaktowalnym, nieablaktowalnymi
    ablativus, ablativach, ablativami, ablativem, ablativie, ablativom, ablativowi, ablativów, ablativu, ablativy, ablatiwie
    ablatiwus, ablatiwach, ablatiwami, ablatiwem, ablatiwie, ablatiwom, ablatiwowi, ablatiwów, ablatiwu, ablatiwy
    ablatyw, ablatywach, ablatywami, ablatywem, ablatywie, ablatywom, ablatywowi, ablatywów, ablatywu, ablatywy
    ablatywny, ablatywna, ablatywną, ablatywne, ablatywnego, ablatywnej, ablatywnemu, ablatywni, ablatywnych, ablatywnym, ablatywnymi, nieablatywna, nieablatywną, nieablatywne, nieablatywnego, nieablatywnej, nieablatywnemu, nieablatywni, nieablatywny, nieablatywnych, nieablatywnym, nieablatywnymi
    ablegat, ablegaci, ablegacie, ablegata, ablegatach, ablegatami, ablegatem, ablegatom, ablegatowi, ablegatów, ablegaty
    ablegier, ablegra, ablegrach, ablegrami, ablegrem, ablegrom, ablegrowi, ablegrów, ablegry, ablegrze
    ablucja, ablucjach, ablucjami, ablucją, ablucje, ablucję, ablucji, ablucjo, ablucjom, ablucyj
    ablutomania, ablutomaniach, ablutomaniami, ablutomanią, ablutomanie, ablutomanię, ablutomanii, ablutoma

    $ pydic_create.py -f sjp.10.txt -v
    Generating sjp.10 dictionary in folder sjp.10.pydic
    [ 1 ] ablaktacja
    [ 2 ] ablaktowalny
    [ 3 ] ablativus
    [ 4 ] ablatiwus
    [ 5 ] ablatyw
    [ 6 ] ablatywny
    [ 7 ] ablegat
    [ 8 ] ablegier
    [ 9 ] ablucja
    [ 10 ] ablutomania

You can also run this command using ``stdin``::

    $ cat sjp.10.txt | pydic_create.py -v
    Generating sjp.10 dictionary in folder sjp.10.pydic
    [ 1 ] ablaktacja
    [ 2 ] ablaktowalny
    [ 3 ] ablativus
    [ 4 ] ablatiwus
    [ 5 ] ablatyw
    [ 6 ] ablatywny
    [ 7 ] ablegat
    [ 8 ] ablegier
    [ 9 ] ablucja
    [ 10 ] ablutomania


.. warning::

    Remember to use ``-n`` option to give a name for a dictionary when using ``stdin`` input.