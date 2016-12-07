# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from datetime import datetime

import arrow

from main.templatetags.main_extras import arrow_filter, utc_to_local_filter, date_formatted_filter, attr_filter

from main.tests.base import BaseTestCase


class ArrowFilterTestCase(BaseTestCase):
    def test_common(self):
        dt = arrow.get(datetime(2016, 12, 12, 12, 12, 12))

        self.assertEquals(arrow_filter(datetime(2016, 12, 12, 12, 12, 12)), dt)
        self.assertEquals(arrow_filter(arrow_filter(datetime(2016, 12, 12, 12, 12, 12))), dt)
        self.assertEquals(arrow_filter('2016-12-12 12:12:12'), dt)

        self.assertEquals(arrow_filter(None), None)
        self.assertEquals(arrow_filter(''), None)


class UTCToLocalFilterTestCase(BaseTestCase):
    def test_common(self):
        dt = arrow.get(datetime(2016, 12, 12, 12, 12, 12)).to('America/Sao_Paulo')

        self.assertEquals(utc_to_local_filter(datetime(2016, 12, 12, 12, 12, 12), 'America/Sao_Paulo'), dt)
        self.assertEquals(utc_to_local_filter('2016-12-12 12:12:12', 'America/Sao_Paulo'), dt)

        self.assertEquals(utc_to_local_filter(None, None), None)
        self.assertEquals(utc_to_local_filter('2016-12-12 12:12:12', None), None)
        self.assertEquals(utc_to_local_filter('', 'America/Sao_Paulo'), None)


class DateFormattedFilterTestCase(BaseTestCase):
    def test_common(self):
        dt = arrow.get(datetime(2016, 12, 12, 12, 12, 12)).to('America/Sao_Paulo')

        self.assertEquals(date_formatted_filter(dt), '2016-12-12 10:12:12 BRST')

        self.assertEquals(date_formatted_filter(None), '')
        self.assertEquals(date_formatted_filter(''), '')


class AttrFilterTestCase(BaseTestCase):
    def test_common(self):
        dt = arrow.get(datetime(2016, 12, 12, 12, 12, 12)).to('America/Sao_Paulo')

        self.assertEquals(attr_filter(dt, 'year'), 2016)

        self.assertEquals(attr_filter(None, 'year'), None)
        self.assertEquals(attr_filter(dt, ''), None)

        self.assertRaises(AttributeError, attr_filter, dt, 'INVALID')
