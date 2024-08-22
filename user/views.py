from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View

from user.forms import LoginForm, RegisterModelForm

from config.settings import EMAIL_DEFAULT_SENDER
from user.forms import LoginForm, RegisterModelForm, SendingEmailForm


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('project_management')
            else:
                messages.error(request, 'Invalid Username or Password')
    else:
        form = LoginForm()
    return render(request, 'ecommerce/auth/login.html', {'form': form})


def register_page(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('ecommerce')
    else:
        form = RegisterModelForm()
    context = {'form': form}
    return render(request, 'ecommerce/auth/register.html', context)


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_page')


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
        if 'send_another' in request.POST:
            return redirect('sending_email')
        context = {
            'form': form,
            'sent': self.sent
        }
        return render(request, 'user/send-email.html', context)
