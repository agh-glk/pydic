#!/usr/bin/env python
# -*- coding: utf8 -*-
import unittest
from pydic.accents import Accents


class TestAccents(unittest.TestCase):
    def setUp(self):
        self.accents = Accents()


    def test_name(self):
        self.assertEquals(set(
            [u'Żolty', u'Żólty', u'Żółty', u'Zólty', u'Zółty', u'Żołty', u'Zołty',
             u'Źolty', u'Źólty', u'Źółty', u'Źołty', ]),
                          set(self.accents.make_accents(u'Zolty'))
        )
