# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from dlogr.exceptions import DlogrAPIError

from django import forms

from main.constants import TIMEZONE_CHOICES
from main.utils import get_dlogr_client


class APIValidationError(forms.ValidationError):
    def __init__(self, code=None, params=None):
        super(APIValidationError, self).__init__(None, code, params)


class APIInternalError(forms.ValidationError):
    message = 'Ups, API is acting up. Please drink a coffe while our trained hamsters fix that.'

    def __init__(self, code=None, params=None):
        super(APIInternalError, self).__init__(self.message, code, params)


class SigninForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        cleaned_data = super(SigninForm, self).clean(*args, **kwargs)

        client = get_dlogr_client()

        try:
            response = client.Auth.login(email=cleaned_data.get('email'), password=cleaned_data.get('password'))
        except DlogrAPIError:
            raise APIInternalError()

        if response.status_code != 200:
            self.api_errors = response.json()
            raise APIValidationError()

        self.user_data = response.json()

        return cleaned_data


class SignupForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    timezone = forms.ChoiceField(choices=TIMEZONE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        cleaned_data = super(SignupForm, self).clean(*args, **kwargs)

        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Passwords did not match.')

        client = get_dlogr_client()
        try:
            response = client.Customer.create(
                email=cleaned_data.get('email'),
                password=cleaned_data.get('password'),
                name=cleaned_data.get('name'),
                timezone=cleaned_data.get('timezone'),
            )
        except DlogrAPIError:
            raise APIInternalError()

        if response.status_code != 201:
            self.api_errors = response.json()
            raise APIValidationError()

        self.user_data = response.json()

        return cleaned_data


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean(self, *args, **kwargs):
        cleaned_data = super(ResetPasswordForm, self).clean(*args, **kwargs)

        client = get_dlogr_client()
        try:
            response = client.Auth.reset_password(email=cleaned_data.get('email'))
        except DlogrAPIError:
            raise APIInternalError()

        if response.status_code != 204:
            self.api_errors = response.json()
            raise APIValidationError()

        return cleaned_data


class ChangeForgottenPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, reset_token, *args, **kwargs):
        super(ChangeForgottenPasswordForm, self).__init__(*args, **kwargs)
        self.reset_token = reset_token

    def clean(self, *args, **kwargs):
        cleaned_data = super(ChangeForgottenPasswordForm, self).clean(*args, **kwargs)

        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Passwords did not match.')

        client = get_dlogr_client()
        try:
            response = client.Auth.change_password(reset_token=self.reset_token, new_password=cleaned_data['password'])
        except DlogrAPIError:
            raise APIInternalError()

        if response.status_code != 200:
            self.api_errors = response.json()
            raise APIValidationError()

        return cleaned_data


class SettingsForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    timezone = forms.ChoiceField(choices=TIMEZONE_CHOICES)

    def __init__(self, user, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self, *args, **kwargs):
        cleaned_data = super(SettingsForm, self).clean(*args, **kwargs)

        client = get_dlogr_client(auth_token=self.user['auth_token'])
        try:
            response = client.Customer.update(
                self.user['id'],
                email=cleaned_data.get('email'),
                name=cleaned_data.get('name'),
                timezone=cleaned_data.get('timezone'),
            )
        except DlogrAPIError:
            raise APIInternalError()

        if response.status_code != 200:
            self.api_errors = response.json()
            raise APIValidationError()

        self.user_data = response.json()

        return cleaned_data


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    new_password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self, *args, **kwargs):
        cleaned_data = super(ChangePasswordForm, self).clean(*args, **kwargs)

        if cleaned_data['new_password'] != cleaned_data['new_password2']:
            raise forms.ValidationError('Passwords did not match.')

        client = get_dlogr_client()
        try:
            response = client.Auth.change_password(
                email=self.user['email'],
                password=cleaned_data['password'],
                new_password=cleaned_data['new_password'],
            )
        except DlogrAPIError:
            raise APIInternalError()

        if response.status_code != 200:
            self.api_errors = response.json()
            raise APIValidationError()

        return cleaned_data
