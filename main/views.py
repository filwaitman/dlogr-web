# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from dlogr.exceptions import DlogrAPIError

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, FormView, RedirectView

from main.forms import (
    APIInternalError, SigninForm, SignupForm, ResetPasswordForm, ChangeForgottenPasswordForm,
    SettingsForm, ChangePasswordForm
)
from main.mixins import AuthTokenRequiredMixin, UnauthTokenRequiredMixin, BaseViewMixin
from main.utils import get_dlogr_client


class IndexView(BaseViewMixin, TemplateView):
    template_name = 'index.html'
    context_data = {'page': 'main', 'keep_unauthed_navbar': True}


class AboutView(BaseViewMixin, TemplateView):
    template_name = 'about.html'
    context_data = {'page': 'about'}


class TermsView(BaseViewMixin, TemplateView):
    template_name = 'terms.html'
    context_data = {'page': 'terms'}


class SupportUsView(BaseViewMixin, TemplateView):
    template_name = 'support-us.html'
    context_data = {'page': 'support-us'}


class HeroesView(BaseViewMixin, TemplateView):
    template_name = 'heroes.html'
    context_data = {'page': 'heroes'}


class WelcomeView(BaseViewMixin, AuthTokenRequiredMixin, TemplateView):
    template_name = 'welcome.html'
    context_data = {'page': 'welcome'}


class SigninView(BaseViewMixin, UnauthTokenRequiredMixin, FormView):
    template_name = 'signin.html'
    form_class = SigninForm
    success_url = reverse_lazy('dashboard')
    context_data = {'page': 'signin'}

    def form_valid(self, form, *args, **kwargs):
        self.set_session_user_data(form.user_data)
        return super(SigninView, self).form_valid(form, *args, **kwargs)


class SignoutView(BaseViewMixin, UnauthTokenRequiredMixin, RedirectView):
    url = reverse_lazy('index')


class SignupView(BaseViewMixin, UnauthTokenRequiredMixin, FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('welcome')
    context_data = {'page': 'signup'}

    def form_valid(self, form, *args, **kwargs):
        self.set_session_user_data(form.user_data)
        return super(SignupView, self).form_valid(form, *args, **kwargs)


class DashboardView(BaseViewMixin, AuthTokenRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    context_data = {'page': 'dashboard'}

    def get_context_data(self, *args, **kwargs):
        context_data = super(DashboardView, self).get_context_data(*args, **kwargs)
        client = get_dlogr_client(auth_token=self.request.session['user']['auth_token'])

        search = self.request.GET.get('search', '')
        context_data['search'] = search

        try:
            context_data['events'] = client.Event.list(search=search).json()
            context_data['api_ok'] = True
        except DlogrAPIError:
            messages.error(self.request, APIInternalError.message)
            context_data['api_ok'] = False

        return context_data


class DashboardDetailView(BaseViewMixin, AuthTokenRequiredMixin, TemplateView):
    template_name = 'dashboard_detail.html'
    context_data = {'page': 'dashboard'}

    def get_context_data(self, *args, **kwargs):
        context_data = super(DashboardDetailView, self).get_context_data(*args, **kwargs)
        client = get_dlogr_client(auth_token=self.request.session['user']['auth_token'])

        object_type = kwargs['object_type']
        object_id = kwargs['object_id']

        try:
            response = client.Event.list(object_type=object_type, object_id=object_id).json()
            context_data['events'] = response
            context_data['api_ok'] = True

            if response['count']:
                context_data['has_results'] = True
                context_data['human_identifier'] = response['results'][0]['human_identifier']
            else:
                messages.warning(self.request, 'No events found for this object.')
                context_data['has_results'] = False
                context_data['human_identifier'] = object_id

        except DlogrAPIError:
            messages.error(self.request, APIInternalError.message)
            context_data['api_ok'] = False

        return context_data


class ResetPasswordView(BaseViewMixin, UnauthTokenRequiredMixin, FormView):
    template_name = 'reset-password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('reset-password')
    context_data = {'page': 'reset-password'}

    def form_valid(self, form, *args, **kwargs):
        email = form.cleaned_data.get('email')
        messages.info(self.request, 'An email has been sent to {} with reset password instructions.'.format(email))
        return super(ResetPasswordView, self).form_valid(form, *args, **kwargs)


class ChangeForgottenPasswordView(BaseViewMixin, UnauthTokenRequiredMixin, FormView):
    template_name = 'change-forgotten-password.html'
    form_class = ChangeForgottenPasswordForm
    success_url = reverse_lazy('signin')
    context_data = {'page': 'change-forgotten-password'}

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ChangeForgottenPasswordView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['reset_token'] = self.request.GET.get('reset_token', 'INVALID')
        return form_kwargs

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Password changed successfully.')
        return super(ChangeForgottenPasswordView, self).form_valid(form, *args, **kwargs)


class VerifyAccountView(BaseViewMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        just_joined = self.request.GET.get('joined', '').lower() == 'true'
        token = self.request.GET.get('token')
        client = get_dlogr_client()

        if not token:
            self.display_errors('Invalid request. Please try again.')
            return reverse_lazy('signin')

        try:
            response = client.Auth.verify_account(token=token)
        except DlogrAPIError:
            self.display_errors(APIInternalError.message)
            return reverse_lazy('signin')

        if response.status_code != 200:
            self.display_errors(response.json())
            return reverse_lazy('signin')

        messages.success(self.request, 'Account verified successfully.')
        self.set_session_user_data(response.json())

        if just_joined:
            return reverse_lazy('welcome')

        return reverse_lazy('dashboard')


class SettingsView(BaseViewMixin, AuthTokenRequiredMixin, FormView):
    template_name = 'settings.html'
    form_class = SettingsForm
    success_url = reverse_lazy('settings')
    context_data = {'page': 'settings'}

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(SettingsView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.session['user']
        return form_kwargs

    def form_valid(self, form, *args, **kwargs):
        self.set_session_user_data(form.user_data, keep_existing_info=True)
        messages.success(self.request, 'Info updated successfully.')
        return super(SettingsView, self).form_valid(form, *args, **kwargs)


class ChangePasswordView(BaseViewMixin, AuthTokenRequiredMixin, FormView):
    template_name = 'change-password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('settings')
    context_data = {'page': 'settings'}

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ChangePasswordView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.session['user']
        return form_kwargs

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Password updated successfully.')
        return super(ChangePasswordView, self).form_valid(form, *args, **kwargs)
