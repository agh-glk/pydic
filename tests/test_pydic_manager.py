#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import tempfile
import unittest
from pydic.pydic_create import PyDicCreator
from pydic import PyDicManager


class TestPyDicManager(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.temp_dict1_path = tempfile.mkdtemp()
        self.temp_dict2_path = tempfile.mkdtemp()
        self.dict1_file = open(os.path.join(self.current_dir, 'dict1.txt'))
        self.dict2_file = open(os.path.join(self.current_dir, 'dict2.txt'))
        PyDicCreator().generate(self.dict1_file, self.temp_dict1_path, 'dict1',
                                verbose=False)
        PyDicCreator().generate(self.dict2_file, self.temp_dict2_path, 'dict2',
                                verbose=False)

        return super(TestPyDicManager, self).__init__(methodName)

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
        self.assertEquals(self.dict.id_forms('4@dict1'),
                          [u"pszczoła", u"pszczoły", u"pszczole", u"pszczołę",
                           u"pszczołą", u"pszczoło",
                           u"pszczół", u"pszczołom", u"pszczołami",
                           u"pszczołach", ])
        self.assertEquals(self.dict.id_forms('8@dict2'),
                          [u"spodnie", u"spodni", u"spodniom", u"spodniami",
                           u"spodniach",
                          ])
        self.assertEquals(self.dict.id_forms('88888888@dict2'), [])

    def test_id_base(self):
        self.assertEquals(self.dict.id_base('6@dict2'), self.dict.id_base('1@dict1'))
        self.assertEquals(self.dict.id_base('4@dict1'), u"pszczoła")
        self.assertEquals(self.dict.id_base('8@dict2'), u"spodnie")
        self.assertEquals(self.dict.id_base('88888888@dict2'), None)

    def test_word_forms(self):
        self.assertEquals(self.dict.word_forms(u'psem'), [(u"pies", u"psa", u"psu",
                                                           u"psem", u"psie",
                                                           u"psy", u"psów",
                                                           u"psom", u"psami",
                                                           u"psach",)])

    def test_word_base(self):
        self.assertEquals(self.dict.word_base(u'psem'), [u"pies"])
        self.assertEquals(self.dict.word_base(u'pilotem'), [u"pilot"])
        self.assertEquals(self.dict.word_base(u'pilotemmmmmm'), [])
        self.assertEquals(set(self.dict.word_base(u'płaszcz')),
                          set([u"płaszczyć", u"płaszcz"]))
                          
    def test_a_id(self):
        self.assertEquals(self.dict.a_id(u'pszczola'),[u"4@dict1"])
        self.assertEquals(self.dict.a_id(u'psow'), [u"2@dict1",u"7@dict2"])
        self.assertEquals(self.dict.a_id(u'psów'), [u"2@dict1",u"7@dict2"])
        self.assertEquals(self.dict.a_id(u'pśów'), [])
		
    def test_a_word_forms(self):
        self.assertEquals(self.dict.a_word_forms(u'psow'), [(u"pies", u"psa", u"psu",
                                                           u"psem", u"psie",
                                                           u"psy", u"psów",
                                                           u"psom", u"psami",
                                                           u"psach",)])

        self.assertEquals(self.dict.a_word_forms(u'pszczol'),
                          [(u"pszczoła", u"pszczoły", u"pszczole", u"pszczołę",
                           u"pszczołą", u"pszczoło",
                           u"pszczół", u"pszczołom", u"pszczołami",
                           u"pszczołach",)])
        self.assertEquals(self.dict.a_word_forms(u'pszczól'),
                          [(u"pszczoła", u"pszczoły", u"pszczole", u"pszczołę",
                           u"pszczołą", u"pszczoło",
                           u"pszczół", u"pszczołom", u"pszczołami",
                           u"pszczołach",)])
        self.assertEquals(self.dict.a_word_forms(u'pszcżól'),
                          [])
                         
    def test_a_word_base(self):
        self.assertEquals(self.dict.a_word_base(u'pszczol'),[u"pszczoła"])
        self.assertEquals(self.dict.a_word_base(u'autopilotow'),[u"autopilot"])
        self.assertEquals(self.dict.a_word_base(u'autopilotów'),[u"autopilot"])
        self.assertEquals(self.dict.a_word_base(u'autopiłotow'),[])
		
    def test_pydic_id_formats(self):
        self.assertRaises(ValueError, self.dict.id_forms, 88888888)
        
