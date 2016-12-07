from django.conf.urls import url

from main.views import (
    IndexView, AboutView, TermsView, SupportUsView, HeroesView, WelcomeView,
    SigninView, SignoutView, SignupView, DashboardView, DashboardDetailView, ResetPasswordView,
    ChangeForgottenPasswordView, VerifyAccountView, SettingsView, ChangePasswordView
)


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^terms/$', TermsView.as_view(), name='terms'),
    url(r'^support-us/$', SupportUsView.as_view(), name='support-us'),
    url(r'^heroes/$', HeroesView.as_view(), name='heroes'),
    url(r'^welcome/$', WelcomeView.as_view(), name='welcome'),

    url(r'^auth/signin/$', SigninView.as_view(), name='signin'),
    url(r'^auth/signout/$', SignoutView.as_view(), name='signout'),
    url(r'^auth/signup/$', SignupView.as_view(), name='signup'),
    url(r'^auth/reset-password/$', ResetPasswordView.as_view(), name='reset-password'),
    url(r'^auth/change-forgotten-password/$', ChangeForgottenPasswordView.as_view(), name='change-forgotten-password'),
    url(r'^auth/verify-account/$', VerifyAccountView.as_view(), name='verify-account'),

    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^dashboard/(?P<object_type>.+)/(?P<object_id>.+)$', DashboardDetailView.as_view(), name='dashboard-detail'),

    url(r'^settings/password/$', ChangePasswordView.as_view(), name='change-password'),
    url(r'^settings/$', SettingsView.as_view(), name='settings'),
]
