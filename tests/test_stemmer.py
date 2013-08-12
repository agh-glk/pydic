#!/usr/bin/env python
# -*- coding: utf8 -*-
import unittest
from pydic.pydic_stemmer import PydicStemmer
from pydic import PyDic


class TestStemmer(unittest.TestCase):
    def setUp(self):
        self.stemmer = PydicStemmer()
        self.dictionary = PyDic('dict1.txt')
        self.index = self.stemmer.build_index(self.dictionary)

    def test_build_index(self):
        self.assertTrue(u'tok' in self.index)
        self.assertTrue(u'seip' in self.index)
        self.assertTrue(u'ywoteloifartlu' in self.index)

    def test_find_base_word(self):
        self.assertEqual(self.stemmer.find_base_word(self.index, u'mełkot'),
                         (5, u'bełkot'))

        self.assertEqual(self.stemmer.find_base_word(self.index, u'sadfasdf'),
                         None)

    def test_inflect(self):
        self.assertEqual(
            self.stemmer.inflect(
                [u'bełkot', u'bełkotu', u'bełkotem', u'bełkotowi', ],
                u'rwałkot'),
            [u'rwałkot', u'rwałkotu', u'rwałkotem', u'rwałkotowi', ]
        )

    def test_process(self):
        self.assertSequenceEqual(
            self.stemmer.process(self.dictionary, self.index, u'rwałkot'),
            [
                u"rwałkot", u"rwałkotu", u"rwałkotowi", u"rwałkotem",
                u"rwałkocie", u"rwałkoty", u"rwałkotów",
                u"rwałkotom", u"rwałkotami", u"rwałkotach",
            ]
        )
