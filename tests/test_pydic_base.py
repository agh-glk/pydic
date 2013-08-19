#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import tempfile
import unittest
import operator
from pydic.pydic_create import PyDicCreator
from pydic import PyDic, PyDicId


class TestPyDicId(unittest.TestCase):
    def test_init_text(self):
        p = PyDicId('123@aaa')
        self.assertEqual(p.id, 123)
        self.assertEqual(p.dict, u'aaa')

    def test_init(self):
        p = PyDicId(123, 'aaa')
        self.assertEqual(p.id, 123)
        self.assertEqual(p.dict, u'aaa')

    def test_error(self):
        self.assertRaises(ValueError, PyDicId)

    def test_str(self):
        p = PyDicId('123@aaa')
        self.assertEqual(str(p), '123@aaa')

    def test_repr(self):
        p = PyDicId('123@aaa')
        self.assertEqual(repr(p), 'PyDicId(u\'123@aaa\')')

    def test_eq(self):
        p = PyDicId('123@aaa')
        q = PyDicId('123@aaa')
        r = PyDicId('124@aaa')
        s = PyDicId('124@baa')
        self.assertTrue(p == q)
        self.assertFalse(p == r)
        self.assertFalse(r == s)

    def test_eq_str(self):
        p = PyDicId('123@aaa')

        self.assertTrue('123@aaa' == p)
        self.assertTrue(p == '123@aaa')
        self.assertFalse(p == '124@aaa')

    def test_eq_err(self):
        p = PyDicId('123@aaa')
        self.assertRaises(TypeError, operator.eq, p, 123)


class TestPyDicBase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.temp_dict1_path = tempfile.mkdtemp()
        self.dict1_file = open(os.path.join(self.current_dir, 'dict1.txt'))
        PyDicCreator().generate(self.dict1_file, self.temp_dict1_path, 'dict1',
                                verbose=False)

        self.dict1 = PyDic(self.temp_dict1_path)
        self.dict1m = PyDic('dict1.txt')

        return super(TestPyDicBase, self).__init__(methodName)

    # def setUp(self):


    def test_file_load(self):
        dict1 = PyDic('dict1.txt')
        self.assertEquals(dict1.id(u'kotem'), ['1@dict1.txt'])
        self.assertEquals(dict1.id(u'utrafieniu'), ['7@dict1.txt'])
        self.assertEquals(dict1.id(u'pszczoły'), ['4@dict1.txt'])
        self.assertEquals(dict1.id(u'spodniami'), ['3@dict1.txt'])
        self.assertEquals(dict1.id(u'piloty'), ['11@dict1.txt', '12@dict1.txt'])
        self.assertEquals(dict1.id(u'piloci'), ['10@dict1.txt'])

    def test_name(self):
        self.assertEquals(self.dict1.name, 'dict1')
        self.assertEquals(self.dict1m.name, 'dict1.txt')

    def test_id(self):
        self.assertEquals(self.dict1.id(u'kotem'), ['1@dict1'])
        self.assertEquals(self.dict1.id(u'utrafieniu'), ['7@dict1'])
        self.assertEquals(self.dict1.id(u'pszczoły'), ['4@dict1'])
        self.assertEquals(self.dict1.id(u'spodniami'), ['3@dict1'])
        self.assertEquals(self.dict1.id(u'piloty'), ['11@dict1', '12@dict1'])
        self.assertEquals(self.dict1.id(u'piloci'), ['10@dict1'])

        self.assertEquals(self.dict1m.id(u'kotem'), ['1@dict1.txt'])
        self.assertEquals(self.dict1m.id(u'utrafieniu'), ['7@dict1.txt'])
        self.assertEquals(self.dict1m.id(u'pszczoły'), ['4@dict1.txt'])
        self.assertEquals(self.dict1m.id(u'spodniami'), ['3@dict1.txt'])
        self.assertEquals(self.dict1m.id(u'piloty'), ['11@dict1.txt', '12@dict1.txt'])
        self.assertEquals(self.dict1m.id(u'piloci'), ['10@dict1.txt'])

    def test_a_id(self):
        self.assertEquals(self.dict1.a_id(u'pszczoly'), ['4@dict1'])

        self.assertEquals(self.dict1m.a_id(u'pszczoly'), ['4@dict1.txt'])


    def test_id_forms(self):
        self.assertEquals(self.dict1.id_forms(PyDicId('4@dict1')),
                          [u"pszczoła", u"pszczoły", u"pszczole", u"pszczołę",
                           u"pszczołą", u"pszczoło",
                           u"pszczół", u"pszczołom", u"pszczołami",
                           u"pszczołach", ])
        self.assertEquals(self.dict1.id_forms(PyDicId('3@dict1')),
                          [u"spodnie", u"spodni", u"spodniom", u"spodniami",
                           u"spodniach", ])
        self.assertEquals(self.dict1.id_forms(PyDicId('30000@dict1')), [])


        self.assertEquals(self.dict1m.id_forms(PyDicId('4@dict1.txt')),
                          [u"pszczoła", u"pszczoły", u"pszczole", u"pszczołę",
                           u"pszczołą", u"pszczoło",
                           u"pszczół", u"pszczołom", u"pszczołami",
                           u"pszczołach", ])
        self.assertEquals(self.dict1m.id_forms(PyDicId('3@dict1.txt')),
                          [u"spodnie", u"spodni", u"spodniom", u"spodniami",
                           u"spodniach", ])
        self.assertEquals(self.dict1m.id_forms(PyDicId('30000@dict1.txt')), [])




    def test_word_forms(self):
        self.assertEquals(self.dict1.word_forms(u"pszczołę"), [
            [u"pszczoła", u"pszczoły", u"pszczole", u"pszczołę",
             u"pszczołą", u"pszczoło",
             u"pszczół", u"pszczołom", u"pszczołami",
             u"pszczołach", ]])
        self.assertEquals(self.dict1.word_forms(u"spodniach"), [
            [u"spodnie", u"spodni", u"spodniom", u"spodniami", u"spodniach",
            ]])
        self.assertEquals(self.dict1.word_forms(u"spodniachhhhhhhh"), [])


        self.assertEquals(self.dict1m.word_forms(u"pszczołę"), [
            [u"pszczoła", u"pszczoły", u"pszczole", u"pszczołę",
             u"pszczołą", u"pszczoło",
             u"pszczół", u"pszczołom", u"pszczołami",
             u"pszczołach", ]])
        self.assertEquals(self.dict1m.word_forms(u"spodniach"), [
            [u"spodnie", u"spodni", u"spodniom", u"spodniami", u"spodniach",
            ]])
        self.assertEquals(self.dict1m.word_forms(u"spodniachhhhhhhh"), [])




    def test_a_word_forms(self):
        self.assertEquals(self.dict1.a_word_forms(u"pszczole"), [
            [u"pszczoła", u"pszczoły", u"pszczole", u"pszczołę", u"pszczołą",
             u"pszczoło", u"pszczół", u"pszczołom",
             u"pszczołami", u"pszczołach", ]])
        self.assertEquals(self.dict1.a_word_forms(u"spodniach"), [
            [u"spodnie", u"spodni", u"spodniom", u"spodniami", u"spodniach",
            ]])
        self.assertEquals(self.dict1.a_word_forms(u"spodniachhhhhhhh"), [])

        self.assertEquals(self.dict1m.a_word_forms(u"pszczole"), [
            [u"pszczoła", u"pszczoły", u"pszczole", u"pszczołę", u"pszczołą",
             u"pszczoło", u"pszczół", u"pszczołom",
             u"pszczołami", u"pszczołach", ]])
        self.assertEquals(self.dict1m.a_word_forms(u"spodniach"), [
            [u"spodnie", u"spodni", u"spodniom", u"spodniami", u"spodniach",
            ]])
        self.assertEquals(self.dict1m.a_word_forms(u"spodniachhhhhhhh"), [])


    def test_empty_label_word_forms(self):
        self.assertEquals(self.dict1.word_forms(u"abakusem"), [
            [u"abakus", u"abakusa", u"abakusach", u"abakusami", u"abakusem", u"abakusie",
             u"abakusom", u"abakusowi", u"abakusów", u"abakusy"]])

        self.assertEquals(self.dict1m.word_forms(u"abakusem"), [
            [u"abakus", u"abakusa", u"abakusach", u"abakusami", u"abakusem", u"abakusie",
             u"abakusom", u"abakusowi", u"abakusów", u"abakusy"]])

    def test_dic_name(self):
        self.assertEquals(self.dict1.name, u"dict1")
        self.assertEquals(self.dict1m.name, u"dict1.txt")

    def test_dic_len(self):
        self.assertEquals(len(self.dict1), 17)
        self.assertEquals(len(self.dict1m), 17)


    def test_id_base(self):
        self.assertEquals(self.dict1.id_base(PyDicId('2@dict1')), u"pies")
        self.assertEquals(self.dict1.id_base(PyDicId('2000@dict1')), None)

    def test_word_base(self):
        self.assertEquals(self.dict1.word_base(u"psów"), [u"pies"])
        self.assertEquals(self.dict1.word_base(u"spodniami"), [u"spodnie"])
        self.assertEquals(self.dict1.word_base(u"#"), [])
        self.assertEquals(self.dict1.word_base(u"pilotowi"), [u"pilot"])

    def test_a_word_base(self):
        self.assertEquals(self.dict1.a_word_base(u"psow"), [u"pies"])
        self.assertEquals(self.dict1.a_word_base(u"spodniami"), [u"spodnie"])
        self.assertEquals(self.dict1.a_word_base(u"#"), [])
        self.assertEquals(self.dict1.a_word_base(u"pilotowi"), [u"pilot"])


    def test_lowercase_hash(self):
        self.assertEquals(self.dict1.word_base(u'żoliborzowi'), [u"Żoliborz"])

    def test_iter(self):
        self.assertEqual(list(self.dict1),
                         [PyDicId(u'1@dict1'), PyDicId(u'2@dict1'), PyDicId(u'3@dict1'),
                          PyDicId(u'4@dict1'), PyDicId(u'5@dict1'), PyDicId(u'6@dict1'),
                          PyDicId(u'7@dict1'), PyDicId(u'8@dict1'), PyDicId(u'9@dict1'),
                          PyDicId(u'10@dict1'), PyDicId(u'11@dict1'),
                          PyDicId(u'12@dict1'), PyDicId(u'13@dict1'),
                          PyDicId(u'14@dict1'), PyDicId(u'15@dict1'),
                          PyDicId(u'16@dict1'), PyDicId(u'17@dict1')]
        )


    def test_common_prefix(self):
        self.assertEquals(PyDic.common_prefix(
            ['abakus', 'abakusa', 'abakusowi', 'abakus', 'abakusem', 'abakusie',
             'abakusie', 'abakusy', 'abakusów', 'abakusom', 'abakusy', 'abakusami',
             'abakusach', 'abakusy']),

                          ['abakus', '', 'a', 'owi', '', 'em', 'ie', 'ie', 'y', 'ów',
                           'om', 'y', 'ami', 'ach', 'y']
        )


    def test_different_id_types(self):
        self.assertNotEqual(self.dict1.id_forms(PyDicId('4@dict1')), [])
        self.assertEqual(self.dict1.id_forms(PyDicId('4@dict1')),
                         self.dict1.id_forms('4@dict1'))
        self.assertEqual(self.dict1.id_forms(PyDicId('4@dict1')), self.dict1.id_forms(4))