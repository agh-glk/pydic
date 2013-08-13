#!/usr/bin/env python
# -*- coding: utf8 -*-
import argparse
from genericpath import commonprefix
from itertools import imap, izip, ifilter
import os
import sys
from pydic import PyDic
import marisa_trie


class PydicStemmer(object):
    MIN_SUFFIX = 3
    INDEX_FILENAME = 'stemmer.index'
    MARISA_FORMAT = '<I'

    def run(self):
        """
        Runs as a command line tool
        """
        parser = argparse.ArgumentParser(
            description='Makes inflection of a flat text file with words.')

        parser.add_argument('-d', '--delimiter', default=u',')
        parser.add_argument('-f', '--dictionary-file',
                            help="path to file with text dictionary",
                            required=True)
        parser.add_argument('-t', '--output', help="output file name")

        parser.add_argument('-b', '--base-forms', action="store_true",
                            help="only base forms")
        parser.add_argument('-v', '--verbose', action="store_true",
                            help="debug verbose mode")

        parser.add_argument('input', metavar='FILE',
                            help="filename to process", nargs='?')
        args = parser.parse_args()

        input_stream = sys.stdin
        if args.input:
            input_stream = open(args.input)

        output_stream = sys.stdout
        if args.output:
            output_stream = open(args.output, 'w')

        self.dictionary = PyDic(args.dictionary_file)
        self.index = self.load_index(self.dictionary)

        for line in input_stream:
            line = line.decode('utf-8').strip()
            if line and line[0] != '#':
                print >> output_stream, args.delimiter.join(
                    self.process(self.dictionary, self.index, line,
                                 debug=args.verbose)).encode('utf-8')
            else:
                print >> output_stream, line.encode('utf-8')

    def load_index(self, dictionary):
        if os.path.isfile(dictionary.get_path(PydicStemmer.INDEX_FILENAME)):
            index = marisa_trie.RecordTrie(PydicStemmer.MARISA_FORMAT)
            index.load(dictionary.get_path(PydicStemmer.INDEX_FILENAME))
        else:
            index = self.build_index(dictionary)
            index.save(dictionary.get_path(PydicStemmer.INDEX_FILENAME))
        return index

    def build_index(self, dictionary):
        return marisa_trie.RecordTrie(
            PydicStemmer.MARISA_FORMAT,
            ifilter(
                lambda t: t[0].find(' ') == -1,
                izip(
                    imap(lambda i: dictionary.id_base(i)[::-1].lower(), dictionary),
                    imap(lambda i: (i,), dictionary),
                )
            )
        )

    def inflect(self, vector, word):
        suffix = commonprefix([vector[0][::-1], word[::-1]])
        prefix = word[:-len(suffix)]
        prefix_len = len(vector[0][:-len(suffix)])
        return map(lambda w: prefix + w[prefix_len:], vector)

    def find_base_word(self, index, word, debug=False):
        reversed_word = word[::-1].lower()
        while len(reversed_word) >= self.MIN_SUFFIX:
            k = index.keys(reversed_word)
            if k:
                if debug:
                    print >> sys.stderr, '%s =~ %s(%d), %d match' % (
                        word, reversed_word[::-1], len(reversed_word), len(k))
                return index[k[0]][0][0], k[0][::-1]
            reversed_word = reversed_word[:-1]
        return None

    def process(self, dictionary, index, word, debug=False):
        bword = self.find_base_word(index, word, debug=debug)
        if debug:
            if bword is None:
                print >> sys.stderr, '%s => None' % (word)
            else:
                print >> sys.stderr, '%s => [%d] %s' % (
                    word, bword[0], bword[1])
        if not bword:
            return word,
        return self.inflect(dictionary.id_forms(bword[0]), word)


if __name__ == '__main__':
    try:
        PydicStemmer().run()
    except KeyboardInterrupt:
        pass