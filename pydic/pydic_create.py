#!/usr/bin/env python
# -*- coding: utf8 -*-
import argparse
import os
import sys

from pydic import ConfigurationErrorException, PyDic


class PyDicCreator(object):
    def run(self):
        """
        Runs as a command line tool
        """
        parser = argparse.ArgumentParser(
            description='Generate dictionary from text input.')
        parser.add_argument('-d', '--delimiter', help="delimiter", default=',')
        parser.add_argument('-f', '--dictionary-file',
                            help="path to file with text dictionary")
        parser.add_argument('-t', '--target', help="path to target dictionary directory",
                            default=None)

        parser.add_argument('-n', '--name',
                            help="name of newly created dictionary (default same as text file)")
        parser.add_argument('-v', '--verbose', action="store_true")
        args = parser.parse_args()

        if not args.dictionary_file and not args.name:
            raise ConfigurationErrorException('Name must be provided if using stdin')

        input = sys.stdin
        if args.dictionary_file:
            input = open(args.dictionary_file)

        name = ''
        if args.name:
            name = args.name.decode('utf-8')
        else:
            name = os.path.basename(args.dictionary_file).decode('utf-8')
            if name.endswith('.txt') or name.endswith('.text'):
                name = '.'.join(name.split('.')[0:-1])

        if args.target is None:
            target = "%s.%s" % (name, PyDic.DIR_EXTENSION)
        else:
            target = args.target
        if args.verbose:
            print >> sys.stderr, "Generating", name, "dictionary in folder", target
        self.generate(input, target, name, delimiter=args.delimiter,
                      verbose=args.verbose)

    def generate(self, from_source, to_path, name, delimiter=',', verbose=False):

        PyDic.make_pydic_index(from_source=from_source,
                               to_path=to_path,
                               name=name,
                               delimiter=delimiter,
                               verbose=verbose)


if __name__ == '__main__':
    try:
        PyDicCreator().run()
    except ConfigurationErrorException, e:
        print >> sys.stderr, "!!!Configuration Error:", e
    except KeyboardInterrupt:
        pass