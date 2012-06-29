# -*- coding: utf8 -*-

class AccentsTable:
    PL = {      u'a':  [u'ą'],
                u'c':  [u'ć'],
                u'e' : [u'ę'],
                u'l' : [u'ł'],
                u'n' : [u'ń'],
                u'o' : [u'ó'],
                u's' : [u'ś'],
                u'z' : [u'ż', u'ź'],

                u'A':  [u'Ą'],
                u'C':  [u'Ć'],
                u'E' : [u'Ę'],
                u'L' : [u'Ł'],
                u'N' : [u'Ń'],
                u'O' : [u'Ó'],
                u'S' : [u'Ś'],
                u'Z' : [u'Ż', u'Ź'],

                }
class Accents:
    """
    Class used to add accents to plain words
    """
    def make_accents(self, word, mapping=AccentsTable.PL, pos=0):
        """
        Generate a list of possible accents variations of word.

        :param word: word
        :type word: unicode
        :param mapping: mapping dictionary
        :return: list of word variations using accents
        """
        word_list = []
        if len(word) > 20:
            return []
        for i in xrange(pos, len(word)):
            if word[i] in mapping:
                for accent in mapping[word[i]]:
                    next_word = word[0:i] + accent + word[i+1:]
                    word_list += [next_word] + self.make_accents(next_word, pos=i)
        return word_list