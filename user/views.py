from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from config.settings import EMAIL_DEFAULT_SENDER
from user.forms import LoginForm, RegisterModelForm, SendingEmailForm
from user.authentication_form import AuthenticationForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from user.models import User
from user.tokens import account_activation_token


class LoginPage(LoginView):
    redirect_authenticated_user = True
    form_class = AuthenticationForm
    template_name = 'ecommerce/auth/login.html'

    def get_success_url(self):
        return reverse_lazy('customers')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password')
        return self.render_to_response(self.get_context_data(form=form))


class RegisterPage(FormView):
    template_name = 'ecommerce/auth/register.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        current_site = get_current_site(self.request)
        message = render_to_string('user/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email = EmailMessage(
            'Activate Your Account',
            message,
            EMAIL_DEFAULT_SENDER,
            [user.email],
        )
        email.content_subtype = 'html'
        email.send()

        return HttpResponse('''
            <html>
            <head>
                <title>Registration Confirmation</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        color: #333;
                        margin: 0;
                        padding: 20px;
                    }
                    .container {
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        text-align: center;
                    }
                    h1 {
                        color: #4CAF50;
                    }
                    p {
                        line-height: 1.6;
                        font-size: 16px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Thank You!</h1>
                    <p>Please confirm your email address by clicking the link sent to your email to complete the registration process.</p>
                </div>
            </body>
            </html>
        ''')


class LogoutPage(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('customers')


class SendingEmail(View):
    sent = False

    def get(self, request, *args, **kwargs):
        form = SendingEmailForm()
        context = {
            'form': form,
            'sent': self.sent
        }
        return render(request, 'user/send-email.html', context)

    def post(self, request, *args, **kwargs):
        form = SendingEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient_list = form.cleaned_data['recipient_list']
            send_mail(
                subject,
                message,
                EMAIL_DEFAULT_SENDER,
                recipient_list,
                fail_silently=False
            )
            self.sent = True
        context = {
            'form': form,
            'sent': self.sent
        }
        return render(request, 'user/send-email.html', context)


class ActivateAccount(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponse('''
                <html>
                <head>
                    <title>Account Activation</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            color: #333;
                            margin: 0;
                            padding: 20px;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            background-color: #fff;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                            text-align: center;
                        }
                        h1 {
                            color: #4CAF50;
                        }
                        p {
                            line-height: 1.6;
                            font-size: 16px;
                        }
                        .btn {
                            display: inline-block;
                            padding: 10px 20px;
                            font-size: 16px;
                            color: #fff;
                            background-color: #4CAF50;
                            border-radius: 5px;
                            text-decoration: none;
                            margin-top: 20px;
                        }
                        .btn:hover {
                            background-color: #45a049;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Thank You!</h1>
                        <p>Your email has been successfully confirmed. </p>
                    </div>
                </body>
                </html>
            ''')
        else:
            return HttpResponse('''
                <html>
                <head>
                    <title>Account Activation</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            color: #333;
                            margin: 0;
                            padding: 20px;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            background-color: #fff;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                            text-align: center;
                        }
                        h1 {
                            color: #e74c3c;
                        }
                        p {
                            line-height: 1.6;
                            font-size: 16px;
                        }
                        .btn {
                            display: inline-block;
                            padding: 10px 20px;
                            font-size: 16px;
                            color: #fff;
                            background-color: #e74c3c;
                            border-radius: 5px;
                            text-decoration: none;
                            margin-top: 20px;
                        }
                        .btn:hover {
                            background-color: #c0392b;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Oops!</h1>
                        <p>The activation link is invalid or has expired.</p>
                    </div>
                </body>
                </html>
            ''')
