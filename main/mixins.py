# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import six

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin


class AuthTokenRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return 'user' in self.request.session


class UnauthTokenRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        self.request.session.pop('user', None)
        return True


class ErrorHandlerMixin(object):
    def display_errors(self, errors, expected_fields=None):
        if not expected_fields:
            expected_fields = []

        if isinstance(errors, dict):
            for key, values in errors.items():
                if key in expected_fields:
                    prefix = '{}: '.format(key)
                else:
                    prefix = ''

                if isinstance(values, six.text_type):
                    messages.error(self.request, '{}{}'.format(prefix, values))
                else:
                    for value in values:
                        messages.error(self.request, '{}{}'.format(prefix, value))

        else:
            messages.error(self.request, errors)

    def form_invalid(self, form, *args, **kwargs):
        errors = getattr(form, 'api_errors', form.errors)
        self.display_errors(errors, expected_fields=form.fields.keys())
        return super(ErrorHandlerMixin, self).form_invalid(form, *args, **kwargs)


class ContextDataMixin(object):
    context_data = {}

    def get_context_data(self, *args, **kwargs):
        context_data = super(ContextDataMixin, self).get_context_data(*args, **kwargs)
        context_data.update(self.context_data)
        return context_data


class SessionDataMixin(object):
    def set_session_user_data(self, user_data, keep_existing_info=False):
        if keep_existing_info:
            current_data = self.request.session.get('user', {})
            current_data.update(user_data)
            user_data = current_data

        self.request.session['user'] = {
            'auth_token': user_data['auth_token'],
            'email': user_data['email'],
            'name': user_data['name'],
            'timezone': user_data['timezone'],
            'id': user_data['id'],
        }


class BaseViewMixin(ErrorHandlerMixin, ContextDataMixin, SessionDataMixin):
    pass
