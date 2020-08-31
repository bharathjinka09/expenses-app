from .views import RegistrationView, UsernameValidationView, EmailValidationView, VerificationView, LoginView, LogoutView, RequestResetEmailView,SetNewPasswordView

from django.urls import path

from django.views.decorators.csrf import csrf_exempt

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.sites.shortcuts import get_current_site


urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),

    path('login', LoginView.as_view(), name='login'),

    path('logout', LogoutView.as_view(), name='logout'),


    path('validate-username', csrf_exempt(UsernameValidationView.as_view()),
         name='validate-username'),

    path('validate-email', csrf_exempt(EmailValidationView.as_view()),
         name='validate-email'),

    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),

    path('set-new-password/<uidb64>/<token>', SetNewPasswordView.as_view(), name='set-new-password'),

    path('request-reset-email', RequestResetEmailView.as_view(),
         name='request-reset-email'),

]
