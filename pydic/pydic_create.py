#!/usr/bin/env python
# -*- coding: utf8 -*-
import argparse
from bsddb3 import db
import os
import sys

from pydic import ConfigurationErrorException, NAME_FILENAME, FORMS_HASH_FILENAME, FORMS_RECNO_FILENAME

class PyDicCreator(object):
    def run(self):
        """
        Runs as a command line tool
        """
        parser = argparse.ArgumentParser(description='Generate dictionary from text input.')
        parser.add_argument('-d', '--dictionary-file', help="path to file with text dictionary")
        parser.add_argument('-t', '--target',  help="path to target dictionary directory", default=".")

        parser.add_argument('-n', '--name',  help="name of newly created dictionary (default same as text file)")
        args = parser.parse_args()

        if not args.dictionary_file and not args.name:
            raise ConfigurationErrorException('Name must be provided if using stdin')

        input = sys.stdin
        if args.dictionary_file:
            input = open(args.dictionary_file)

        name = ''
        if args.name :
            name = args.name.decode('utf-8')
        else:
            name = os.path.basename(args.dictionary_file).decode('utf-8')
            if name.endswith('.txt') or name.endswith('.text'):
                name = '.'.join(name.split('.')[0:-1])


        print >> sys.stderr , "Generating" , name, "dictionary"
        self.generate(input, args.target, name)

    def generate(self, from_source, to_path, name, verbose=True):

        if os.path.exists(os.path.join(to_path, NAME_FILENAME)) or os.path.exists(os.path.join(to_path, NAME_FILENAME)) or os.path.exists(os.path.join(to_path, NAME_FILENAME)):
            raise ConfigurationErrorException('Cowardly refusing to create dictionary in non empty directory')

        if not os.path.exists(to_path):
            os.makedirs(to_path)

        name_file = open(os.path.join(to_path, NAME_FILENAME), 'w')
        name_file.write(name.encode('utf-8') + '\n')
        name_file.close()

        hash = db.DB()
        hash.open(os.path.join(to_path, FORMS_HASH_FILENAME), dbtype=db.DB_HASH, flags=db.DB_CREATE)

        recno = db.DB()
        recno.open(os.path.join(to_path, FORMS_RECNO_FILENAME), dbtype=db.DB_RECNO, flags=db.DB_CREATE)

        for line in from_source:
            bits = line.split(':')
            bits = map(lambda x: x.strip().decode('utf-8'), bits)
            bits = filter(lambda x: x, bits)
            bits = filter(lambda x: x != "#", bits) #filtering non flectional
            if bits:
                bits = [bits[0]] + bits[2:] # avoiding second element which is LABEL
                #save format is <prefix>:bform suffix:form1 suffix:form2 suffix:form3 suffix....
                #bform and form1 will usually be the same

                bits_prefixed = self.common_prefix(bits)
                wid = recno.append((':'.join(bits_prefixed)).encode('utf-8'))
                if verbose:
                    print "[", wid, "]", bits[0]

                for bit in set(bits):

                    form = bit.encode('utf-8')
                    try:
                        hash[form] = "%s:%s" % (hash[form], str(wid))
                    except KeyError:
                        hash[form] = str(wid)

        hash.close()
        recno.close()

    def common_prefix(self, word_list):
        """
        For a list of words produces a list of [optimal prefix, suffix1, suffix2...]
        :param word_list:
        :return:
        """
        i = min (map(lambda x: len(x), word_list))
        while i > 0:
            lst=map(lambda x: x[0:i], word_list)
            # http://stackoverflow.com/questions/3844801
            # Fastest checking if lst has the same values
            if (not lst or lst.count(lst[0]) == len(lst)):
                break
            i -= 1
        return [word_list[0][0:i]] + map(lambda x: x[i:], word_list)




if __name__ == '__main__':
    try:
        PyDicCreator().run()
    except ConfigurationErrorException, e:
        print "!!!Configuration Error:", e
    except KeyboardInterrupt:
        pass