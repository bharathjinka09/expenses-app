from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from validate_email import validate_email
from django.core.mail import EmailMessage
from django.urls import reverse
from secret_file import sender_email, sender_password
from .utils import account_activation_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
import json
from django.contrib.auth.tokens import PasswordResetTokenGenerator



class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid!'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry. Email already taken.Please choose another one! '}, status=409)

        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain letters and numbers'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry. Username already taken.Please choose another one! '}, status=409)

        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request).domain
                link = reverse('activate', kwargs={
                    'uidb64': uidb64, 'token': account_activation_token.make_token(user)
                })

                activate_url = 'http://' + current_site + link

                email_body = f"Hi {user.username}. Please click this link to verify your account!\n {activate_url}"

                email_subject = 'Activate your account'

                # activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    email_body,
                    sender_email,
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            # gives user id
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully!')
            return redirect('login')

        except Exception as e:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:

            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(
                        request, f'Welcome {user.username}. You are logged in!')
                    return redirect('expenses')
                messages.error(
                    request, 'Account is not active. Please check your email!')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid credentials. Please try again!')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Please fill all fields!')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out!')
        return redirect('login')


class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'authentication/request-reset-email.html')

    def post(self, request):
        email = request.POST['email']

        if not validate_email(email):
            messages.error(request, 'Please enter a valid email')

            return render(request, 'authentication/request-reset-email.html')

        user = User.objects.filter(email=email)

        if user.exists():
            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            current_site = get_current_site(request).domain

            link = reverse('request-reset-email', kwargs={
                'uidb64': uidb64, 'token': PasswordResetTokenGenerator.make_token(user)
            })

            activate_url = 'http://' + current_site + link

            email_subject = 'Reset your password'

            email_body = f"Hi {user.username}. Please click this link to reset your password!\n {activate_url}"

            # activate_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                email_body,
                sender_email,
                [email],
            )
            email.send(fail_silently=False)

        messages.success(
            request, 'We have sent you an email with instructions on resetting your password')
        return render(request, 'authentication/request-reset-email.html')


class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        return render(request, 'authentication/request-reset-email.html')
    
    def post(self, request, uidb64, token):
        return render(request, 'authentication/request-reset-email.html')
