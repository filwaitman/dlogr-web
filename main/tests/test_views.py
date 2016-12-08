# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import mock
from dlogr.exceptions import DlogrAPIError

from django.core.urlresolvers import reverse

from main.forms import APIInternalError
from main.tests.base import BaseTestCase
from main.tests.fixtures import (
    CUSTOMER_OBJECT, CUSTOMER_OBJECT_WITH_AUTH_KEY, EVENT_LIST, NO_CONTENT,
    LIST_NO_OBJECTS, EVENT_OBJECT1, EVENT_OBJECT2, EVENT_OBJECT3
)


class SimpleTemplatesTestCase(BaseTestCase):
    def setUp(self):
        super(SimpleTemplatesTestCase, self).setUp()
        self.expected_status_code = 200

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)

    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertEquals(response.status_code, 200)

    def test_terms(self):
        response = self.client.get(reverse('terms'))
        self.assertEquals(response.status_code, 200)

    def test_support_us(self):
        response = self.client.get(reverse('support-us'))
        self.assertEquals(response.status_code, 200)

    def test_heroes(self):
        response = self.client.get(reverse('heroes'))
        self.assertEquals(response.status_code, 200)

    def test_welcome(self):
        self.login()

        response = self.client.get(reverse('welcome'))
        self.assertEquals(response.status_code, 200)


class SigninViewTestCase(BaseTestCase):
    def setUp(self):
        super(SigninViewTestCase, self).setUp()
        self.client_call = self.client_patched().Auth.login
        self.data = {'email': 'filwaitman@gmail.com', 'password': 'password'}
        self.expected_status_code = 200

    def test_get(self):
        response = self.client.get(reverse('signin'))
        self.assertEquals(response.status_code, 200)

    def test_post_success(self):
        response_mocked = mock.Mock(status_code=self.expected_status_code)
        response_mocked.json.return_value = CUSTOMER_OBJECT_WITH_AUTH_KEY
        self.client_call.return_value = response_mocked

        response = self.client.post(reverse('signin'), self.data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['dashboard.html', ])

    def test_invalid_payload(self):
        response_mocked = mock.Mock(status_code=400)
        response_mocked.json.return_value = {'non_field_errors': ['Unable to login with credentials provided.', ]}
        self.client_call.return_value = response_mocked

        response = self.client.post(reverse('signin'), self.data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['signin.html', ])
        self.assertTrue('Unable to login with credentials provided.' in response.content.decode('utf-8'))

    def test_api_out(self):
        self.client_call.side_effect = DlogrAPIError()

        response = self.client.post(reverse('signin'), self.data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['signin.html', ])
        self.assertTrue(APIInternalError.message in response.content.decode('utf-8'))


class SignupViewTestCase(BaseTestCase):
    def setUp(self):
        super(SignupViewTestCase, self).setUp()
        self.client_call = self.client_patched().Customer.create
        self.data = {
            'email': 'filwaitman@gmail.com', 'timezone': 'America/Sao_Paulo', 'name': 'WaitCorp',
            'password': 'password', 'password2': 'password',
        }
        self.expected_status_code = 201

    def test_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)

    def test_post_success(self):
        response_mocked = mock.Mock(status_code=self.expected_status_code)
        response_mocked.json.return_value = CUSTOMER_OBJECT_WITH_AUTH_KEY
        self.client_call.return_value = response_mocked

        response = self.client.post(reverse('signup'), self.data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['welcome.html', ])

    def test_password_mismatch(self):
        data = self.data.copy()
        data['password2'] = 'MISMATCH'

        response = self.client.post(reverse('signup'), data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['signup.html', ])
        self.assertTrue('Passwords did not match.' in response.content.decode('utf-8'))

    def test_invalid_payload(self):
        response_mocked = mock.Mock(status_code=400)
        response_mocked.json.return_value = {'email': ['customer with this email already exists.', ]}
        self.client_call.return_value = response_mocked

        response = self.client.post(reverse('signup'), self.data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['signup.html', ])
        self.assertTrue('email: customer with this email already exists.' in response.content.decode('utf-8'))

    def test_api_out(self):
        self.client_call.side_effect = DlogrAPIError()

        response = self.client.post(reverse('signup'), self.data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['signup.html', ])
        self.assertTrue(APIInternalError.message in response.content.decode('utf-8'))


class DashboardViewTestCase(BaseTestCase):
    def setUp(self):
        super(DashboardViewTestCase, self).setUp()
        self.client_call = self.client_patched().Event.list
        self.expected_status_code = 200

    def test_not_authed(self):
        response = self.client.get(reverse('dashboard'), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['signin.html', ])

    def test_no_events(self):
        self.login()
        response_mocked = mock.Mock(status_code=self.expected_status_code)
        response_mocked.json.return_value = LIST_NO_OBJECTS
        self.client_call.return_value = response_mocked

        response = self.client.get(reverse('dashboard'), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['dashboard.html', ])
        self.assertTrue('<h3>Nothing here - yet.</h3>' in response.content.decode('utf-8'))

    def test_events(self):
        self.login()
        response_mocked = mock.Mock(status_code=self.expected_status_code)
        response_mocked.json.return_value = EVENT_LIST
        self.client_call.return_value = response_mocked

        response = self.client.get(reverse('dashboard'), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['dashboard.html', ])
        self.assertTrue('Last events received' in response.content.decode('utf-8'))
        self.assertFalse('<h3>No items found.</h3>' in response.content.decode('utf-8'))
        self.assertFalse('Search results' in response.content.decode('utf-8'))
        self.assertFalse('[Hit <Enter> to clear current search]' in response.content.decode('utf-8'))

        self.assertTrue(EVENT_OBJECT1['human_identifier'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT1['object_id'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT1['object_type'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT1['message'] in response.content.decode('utf-8'))

        self.assertTrue(EVENT_OBJECT2['human_identifier'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT2['object_id'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT2['object_type'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT2['message'] in response.content.decode('utf-8'))

        self.assertTrue(EVENT_OBJECT3['human_identifier'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT3['object_id'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT3['object_type'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT3['message'] in response.content.decode('utf-8'))

    def test_search(self):
        self.login()
        response_mocked = mock.Mock(status_code=self.expected_status_code)
        response_mocked.json.return_value = EVENT_LIST
        self.client_call.return_value = response_mocked

        response = self.client.get('{}?search=Waitman'.format(reverse('dashboard')), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['dashboard.html', ])
        self.assertTrue('Search results' in response.content.decode('utf-8'))
        self.assertTrue('[Hit <Enter> to clear current search]' in response.content.decode('utf-8'))
        self.assertFalse('Last events received' in response.content.decode('utf-8'))
        self.assertFalse('<h3>No items found.</h3>' in response.content.decode('utf-8'))

        self.assertTrue(EVENT_OBJECT1['human_identifier'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT1['object_id'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT1['object_type'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT1['message'] in response.content.decode('utf-8'))

        self.assertTrue(EVENT_OBJECT2['human_identifier'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT2['object_id'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT2['object_type'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT2['message'] in response.content.decode('utf-8'))

        self.assertTrue(EVENT_OBJECT3['human_identifier'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT3['object_id'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT3['object_type'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT3['message'] in response.content.decode('utf-8'))

    def test_api_out(self):
        self.login()
        self.client_call.side_effect = DlogrAPIError()

        response = self.client.get(reverse('dashboard'), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['dashboard.html', ])
        self.assertTrue(APIInternalError.message in response.content.decode('utf-8'))


class DashboardDetailViewTestCase(BaseTestCase):
    def setUp(self):
        super(DashboardDetailViewTestCase, self).setUp()
        self.client_call = self.client_patched().Event.list
        self.expected_status_code = 200
        self.url = reverse('dashboard-detail', kwargs={'object_type': 'objtype', 'object_id': 'objid'})

    def test_not_authed(self):
        response = self.client.get(self.url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['signin.html', ])

    def test_no_events(self):
        self.login()
        response_mocked = mock.Mock(status_code=self.expected_status_code)
        response_mocked.json.return_value = LIST_NO_OBJECTS
        self.client_call.return_value = response_mocked

        response = self.client.get(self.url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['dashboard_detail.html', ])
        self.assertTrue('No items here - yet.' in response.content.decode('utf-8'))
        self.assertFalse('timeline = new TL.Timeline' in response.content.decode('utf-8'))  # JS initialization

    def test_events(self):
        self.login()
        response_mocked = mock.Mock(status_code=self.expected_status_code)
        response_mocked.json.return_value = EVENT_LIST
        self.client_call.return_value = response_mocked

        response = self.client.get(self.url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['dashboard_detail.html', ])
        self.assertTrue('timeline = new TL.Timeline' in response.content.decode('utf-8'))  # JS initialization
        self.assertFalse('No items here - yet.' in response.content.decode('utf-8'))

        self.assertTrue(EVENT_OBJECT1['human_identifier'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT1['object_id'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT1['object_type'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT1['message'] in response.content.decode('utf-8'))

        self.assertTrue(EVENT_OBJECT2['human_identifier'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT2['object_id'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT2['object_type'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT2['message'] in response.content.decode('utf-8'))

        self.assertTrue(EVENT_OBJECT3['human_identifier'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT3['object_id'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT3['object_type'] in response.content.decode('utf-8'))
        self.assertTrue(EVENT_OBJECT3['message'] in response.content.decode('utf-8'))

    def test_api_out(self):
        self.login()
        self.client_call.side_effect = DlogrAPIError()

        response = self.client.get(self.url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['dashboard_detail.html', ])
        self.assertTrue(APIInternalError.message in response.content.decode('utf-8'))


class SignoutViewTestCase(BaseTestCase):
    def test_get(self):
        response = self.client.get(reverse('signout'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['index.html', ])


class ResetPasswordViewTestCase(BaseTestCase):
    def setUp(self):
        super(ResetPasswordViewTestCase, self).setUp()
        self.client_call = self.client_patched().Auth.reset_password
        self.expected_status_code = 204
        self.data = {'email': 'filwaitman@gmail.com'}
        self.url = reverse('reset-password')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post(self):
        response_mocked = mock.Mock(status_code=self.expected_status_code)
        response_mocked.json.return_value = NO_CONTENT
        self.client_call.return_value = response_mocked

        response = self.client.post(self.url, self.data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(
            'An email has been sent to filwaitman@gmail.com with reset password instructions.' in
            response.content.decode('utf-8')
        )
        self.assertEquals(response.template_name, ['reset-password.html', ])

    def test_invalid_payload(self):
        response_mocked = mock.Mock(status_code=400)
        response_mocked.json.return_value = {
            'I cannot even imagine what could be raised here.'
        }
        self.client_call.return_value = response_mocked

        response = self.client.post(self.url, self.data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTrue('I cannot even imagine what could be raised here.' in response.content.decode('utf-8'))
        self.assertEquals(response.template_name, ['reset-password.html', ])

    def test_api_out(self):
        self.client_call.side_effect = DlogrAPIError()

        response = self.client.post(self.url, self.data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template_name, ['reset-password.html', ])
        self.assertTrue(APIInternalError.message in response.content.decode('utf-8'))


class ChangeForgottenPasswordViewTestCase(BaseTestCase):
    def setUp(self):
        super(ChangeForgottenPasswordViewTestCase, self).setUp()
        self.client_call = self.client_patched().Auth.change_password
        self.expected_status_code = 200
        self.data = {'password': 'password', 'password2': 'password'}
        self.url = '{}?reset_token=wildhash'.format(reverse('change-forgotten-password'))

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post(self):
        response_mocked = mock.Mock(status_code=self.expected_status_code)
        response_mocked.json.return_value = CUSTOMER_OBJECT
        self.client_call.return_value = response_mocked

        response = self.client.post(self.url, self.data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTrue('Password changed successfully.' in response.content.decode('utf-8'))

    def test_password_mismatch(self):
        data = self.data.copy()
        data['password2'] = 'MISMATCH'

        response = self.client.post(self.url, data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTrue('Passwords did not match.' in response.content.decode('utf-8'))

    def test_invalid_payload(self):
        response_mocked = mock.Mock(status_code=400)
        response_mocked.json.return_value = {
            'Reset token is invalid (or has expired).'
        }
        self.client_call.return_value = response_mocked

        response = self.client.post(self.url, self.data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTrue('Reset token is invalid (or has expired).' in response.content.decode('utf-8'))

    def test_api_out(self):
        self.client_call.side_effect = DlogrAPIError()

        response = self.client.post(self.url, self.data, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(APIInternalError.message in response.content.decode('utf-8'))


class VerifyAccountViewTestCase(BaseTestCase):
    def setUp(self):
        super(VerifyAccountViewTestCase, self).setUp()
        self.client_call = self.client_patched().Auth.verify_account
        self.expected_status_code = 200
        self.url = '{}?token=wildhash'.format(reverse('verify-account'))

    def test_get(self):
        response_mocked = mock.Mock(status_code=200)
        response_mocked.json.return_value = CUSTOMER_OBJECT_WITH_AUTH_KEY
        self.client_call.return_value = response_mocked

        response = self.client.get(self.url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTrue('Account verified successfully.' in response.content.decode('utf-8'))
        self.assertEquals(response.template_name, ['dashboard.html', ])

    def test_invalid_payload(self):
        response_mocked = mock.Mock(status_code=400)
        response_mocked.json.return_value = {
            'Reset token is invalid (or has expired).'
        }
        self.client_call.return_value = response_mocked

        response = self.client.get(self.url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTrue('Reset token is invalid (or has expired).' in response.content.decode('utf-8'))
        self.assertEquals(response.template_name, ['signin.html', ])

    def test_api_out(self):
        self.client_call.side_effect = DlogrAPIError()

        response = self.client.get(self.url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(APIInternalError.message in response.content.decode('utf-8'))
        self.assertEquals(response.template_name, ['signin.html', ])
