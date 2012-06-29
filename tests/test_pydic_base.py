#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import tempfile
import unittest
from pydic.pydic_create import PyDicCreator
from pydic_base import PyDic

class TestPyDicBase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.temp_dict1_path = tempfile.mkdtemp()
        self.dict1_file = open(os.path.join(self.current_dir,'dict1.txt'))
        PyDicCreator().generate(self.dict1_file, self.temp_dict1_path, 'dict1', verbose=False)

        return super(TestPyDicBase, self).__init__(methodName)

    def setUp(self):
        self.dict1 = PyDic(self.temp_dict1_path)


    def test_name(self):
        self.assertEquals(self.dict1.name, 'dict1')

    def test_id(self):
        self.assertEquals(self.dict1.id(u'kotem'),      [1])
        self.assertEquals(self.dict1.id(u'utrafieniu'), [7])
        self.assertEquals(self.dict1.id(u'pszczoły'),   [4])
        self.assertEquals(self.dict1.id(u'spodniami'),  [3])
        self.assertEquals(self.dict1.id(u'piloty'),  [11, 12])
        self.assertEquals(self.dict1.id(u'piloci'),  [10])

    def test_id_forms(self):
        self.assertEquals(self.dict1.id_forms(4),   [u"pszczoła", u"pszczoły" , u"pszczole", u"pszczołę", u"pszczołą", u"pszczole", u"pszczoło", u"pszczoły", u"pszczół", u"pszczołom", u"pszczoły", u"pszczołami", u"pszczołach", u"pszczoły",])
        self.assertEquals(self.dict1.id_forms(3),   [u"spodnie", u"spodni", u"spodniom", u"spodnie", u"spodniami",u"spodniach", u"spodnie"])
        self.assertEquals(self.dict1.id_forms(30000),   [])



    def test_word_forms(self):
        self.assertEquals(self.dict1.word_forms(u"pszczołę"),   [[u"pszczoła", u"pszczoły" , u"pszczole", u"pszczołę", u"pszczołą", u"pszczole", u"pszczoło", u"pszczoły", u"pszczół", u"pszczołom", u"pszczoły", u"pszczołami", u"pszczołach", u"pszczoły",]])
        self.assertEquals(self.dict1.word_forms(u"spodniach"),   [[u"spodnie", u"spodni", u"spodniom", u"spodnie", u"spodniami",u"spodniach", u"spodnie"]])
        self.assertEquals(self.dict1.word_forms(u"spodniachhhhhhhh"),   [])

    def test_empty_label_word_forms(self):
        self.assertEquals(self.dict1.word_forms(u"abakusem"),   [[u"abakus", u"abakusa" , u"abakusach", u"abakusami", u"abakusem", u"abakusie", u"abakusom", u"abakusowi", u"abakusów", u"abakusy"]])

    def test_id_base(self):
        self.assertEquals(self.dict1.id_base(2), u"pies")
        self.assertEquals(self.dict1.id_base(2000000), None)

    def test_word_base(self):
        self.assertEquals(self.dict1.word_base(u"psów"), [u"pies"])
        self.assertEquals(self.dict1.word_base(u"spodniami"), [u"spodnie"])
        self.assertEquals(self.dict1.word_base(u"#"), [])
        self.assertEquals(self.dict1.word_base(u"pilotowi"), [u"pilot"])


