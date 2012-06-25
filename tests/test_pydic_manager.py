#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import tempfile
import unittest
from pydic.pydic_create import PyDicCreator
from pydic_manager import PyDicManager

class TestPyDicBase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.temp_dict1_path = tempfile.mkdtemp()
        self.temp_dict2_path = tempfile.mkdtemp()
        self.dict1_file = open(os.path.join(self.current_dir,'dict1.txt'))
        self.dict2_file = open(os.path.join(self.current_dir,'dict2.txt'))
        PyDicCreator().generate(self.dict1_file, self.temp_dict1_path, 'dict1', verbose=False)
        PyDicCreator().generate(self.dict2_file, self.temp_dict2_path, 'dict2', verbose=False)

        return super(TestPyDicBase, self).__init__(methodName)

    def setUp(self):
        self.dict = PyDicManager(self.temp_dict1_path, self.temp_dict2_path)


    def test_dictionaries(self):
        self.assertEquals(set(self.dict.get_dictionaries()), set(['dict1', 'dict2']))

    def test_id(self):
        self.assertEquals(set(self.dict.id(u'kotem')), set(['1@dict1', '6@dict2']))
        self.assertEquals(set(self.dict.id(u'płaszcz')), set(['13@dict1', '9@dict2']))
        self.assertEquals(self.dict.id(u'zatelegrafowałobym'), ['5@dict2'])
        self.assertEquals(self.dict.id(u'zatelegrafowałobymmmmm'), [])

    def test_id_forms(self):
        self.assertEquals(self.dict.id_forms('6@dict2'), self.dict.id_forms('1@dict1'))
        self.assertEquals(self.dict.id_forms('4@dict1'), [u"pszczoła", u"pszczoły" , u"pszczole", u"pszczołę", u"pszczołą", u"pszczole", u"pszczoło", u"pszczoły", u"pszczół", u"pszczołom", u"pszczoły", u"pszczołami", u"pszczołach", u"pszczoły",])
        self.assertEquals(self.dict.id_forms('8@dict2'), [u"spodnie", u"spodni", u"spodniom", u"spodnie", u"spodniami",u"spodniach", u"spodnie"])
        self.assertEquals(self.dict.id_forms('88888888@dict2'), [])

    def test_id_base(self):
        self.assertEquals(self.dict.id_base('6@dict2'), self.dict.id_base('1@dict1'))
        self.assertEquals(self.dict.id_base('4@dict1'), u"pszczoła")
        self.assertEquals(self.dict.id_base('8@dict2'), u"spodnie")
        self.assertEquals(self.dict.id_base('88888888@dict2'), None)

    def test_word_forms(self):
        self.assertEquals(self.dict.word_forms(u'psem'), [(u"pies", u"psa", u"psu", u"psa", u"psem", u"psie", u"psie", u"psy", u"psów", u"psom", u"psy", u"psami", u"psach", u"psy")])

    def test_word_base(self):
        self.assertEquals(self.dict.word_base(u'psem'), [u"pies"])
        self.assertEquals(self.dict.word_base(u'pilotem'), [u"pilot"])
        self.assertEquals(self.dict.word_base(u'pilotemmmmmm'), [])
        self.assertEquals(set(self.dict.word_base(u'płaszcz')), set([u"płaszczyć", u"płaszcz"]))


