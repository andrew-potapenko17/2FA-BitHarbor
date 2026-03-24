from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from .mfa.qrcode import generate_otp_qrcode
from .mfa.mail_code_generation import generate_mail_verification_code
from .mfa.mfa_verification import verify_2fa_otp, verify_mail_code
from .mail.mail import send_verification_mail
from .models import CustomUser

import logging
import pyotp

logger = logging.getLogger(__name__)


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, 'Passwods do not match')
            return redirect('register')

        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()

            code = generate_mail_verification_code(user.id)
            send_verification_mail(email, code)

            return render(request, 'main/mfa_verify.html', {'user_id': user.id, 'type': 'mail'})
        except Exception as e:
            logger.critical(e)
            messages.error(request, "401 Unauthorized Error")
            return redirect('register')
        
    return render(request, 'main/auth_form.html', {'type': 'register'})


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
            if user == None:
                messages.error(request, "Invalid Credantials")
                return redirect('login')
            if user.mfa_enabled:
                return render(request, 'main/otp_verify.html', {'user_id': user.id, 'type': 'otp'})
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('home')
        except Exception as e:
            logger.critical(e, exc_info=True)
            messages.error(request, "401 Unauthorized Error")
            return redirect('login')

    return render(request, 'main/auth_form.html', {'type': 'login'})


@login_required(login_url='login')
def logout_action(request):
    logout(request)
    messages.warning(request, 'Logged out')
    return redirect('login')

    
@login_required(login_url='login')
def home(request):
    user = request.user
    if not user.mfa_secret:
        user.mfa_secret = pyotp.random_base32()
        user.save()
    
    qr = generate_otp_qrcode(mfa_secret=user.mfa_secret, username=user.username)
    return render(request, 'main/home.html', {"qrcode" : qr})


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp_code')
        user_id = request.POST.get('user_id')
        
        try:
            user = CustomUser.objects.get(id=user_id)

            if verify_2fa_otp(user, otp):
                messages.success(request, '2FA Success')
                if not request.user.is_authenticated:
                    login(request, user)
                    messages.success(request, 'Successfully logged in')
                
                return redirect('home')
            else:
                messages.warning(request, 'Invalid mfa code')
                return redirect('login')
        except Exception as e:
            logger.critical(e)
            messages.error(request, "Could not verify mfa")
            return redirect('home')
    
    return render(request, 'main/home.html')


def verify_mail(request):
    if request.method == "POST":
        input_code = request.POST.get('mail_code')
        user_id = request.POST.get('user_id')

        try:
            user = CustomUser.objects.get(id=user_id)
            verify_result = verify_mail_code(user_id, input_code)
            if verify_result == "success":
                user.is_active = True
                user.save()

                login(request, user)
                messages.success(request, "Mail verified")
                return redirect('home')
            else:
                messages.warning(request, verify_result)
                return redirect('verify_mail')
        except Exception as e:
            logger.critical(e)
            messages.error(request, "401 Unauthorized Error")

    return render(request, 'main/mfa_verify.html', {'type': 'mail'})


@login_required(login_url='login')
def disable_2fa(request):
    user = request.user
    if user.mfa_enabled:
        user.mfa_enabled = False
        user.save()
    messages.warning(request, '2FA disabled')
    return redirect('home')