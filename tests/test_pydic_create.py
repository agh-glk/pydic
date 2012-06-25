#!/usr/bin/env python
# -*- coding: utf8 -*-
import unittest
from pydic.pydic_create import PyDicCreator

class TestPyDicCreator(unittest.TestCase):
    def test_common_prefix(self):
        dic = PyDicCreator()

        self.assertEquals(dic.common_prefix(['abakus','abakusa','abakusowi','abakus','abakusem','abakusie','abakusie','abakusy','abakusów','abakusom','abakusy','abakusami','abakusach','abakusy']),

        ['abakus', '', 'a','owi','','em','ie','ie','y','ów','om','y','ami','ach','y']
        )

