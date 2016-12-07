# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import mock

from django.core.urlresolvers import reverse
from django.test import TestCase

from main.tests.fixtures import CUSTOMER_OBJECT_WITH_AUTH_KEY


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()

        self._client_patched = mock.patch('main.utils.DlogrClient')
        self.client_patched = self._client_patched.start()

    def tearDown(self):
        self._client_patched.stop()
        super(BaseTestCase, self).tearDown()

    def login(self):
        response_mocked = mock.Mock(status_code=self.expected_status_code)
        response_mocked.json.return_value = CUSTOMER_OBJECT_WITH_AUTH_KEY
        self.client_patched().Auth.login.return_value = response_mocked

        self.client.post(reverse('signin'), {'email': 'filwaitman@gmail.com', 'password': 'password'}, follow=True)
