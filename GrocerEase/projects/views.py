import hashlib
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Customer
from .forms import RegistrationForm, LoginForm, OTPVerificationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import HttpResponseForbidden
from datetime import timedelta
import re
from django.core.mail import send_mail
import random
from django.urls import reverse


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['customerpassword']

            if not re.match(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$%^&+=!]).{8,}$', password):
                form.add_error('customerpassword', 'Password must contain at least one digit, one uppercase letter, one lowercase letter, and one special character.')
                print("Password regex validation failed")

            try:
                validate_password(password)
            except ValidationError as e:
                form.add_error('customerpassword', e.messages[0])
                print(f"Password validation failed: {e.messages[0]}")
            else:
                user = form.save(commit=False)  # user object in memory
                user.customerpassword = make_password(password)  # password hash
                otp = ''.join(random.choice('0123456789') for _ in range(6))
                user.otp = otp

                request.session['registered_user_email'] = user.customeremail
                request.session['registered_user_name'] = user.customername
                request.session['registered_user_password'] = user.customerpassword
                request.session['otp'] = otp

                send_mail(
                    'GrocerEase OTP Verification',
                    f'Your OTP for account verification is: {otp}',
                    'grocereasedp1@gmail.com',
                    [user.customeremail],
                    fail_silently=False,
                )

                return redirect('verify_otp')  

    else:
        form = RegistrationForm()

    return render(request, 'projects/signup.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '')
        session_otp = request.session.get('otp', None)
        print(entered_otp, session_otp)

        user_email = request.session.get('registered_user_email', None)
        customer_name = request.session.get('registered_user_name', None)  # Add this line
        customer_password = request.session.get('registered_user_password', None)  # Add this line
        print(user_email, customer_name, customer_password)

        if user_email:
            if entered_otp == session_otp:
                user = Customer.objects.create(
                    customername=customer_name,  
                    customeremail=user_email,
                    customerpassword=customer_password,
                    otp=session_otp,  
                    is_verified=True
                )
                return redirect('login')
            else:
                error_message = 'Invalid OTP. Please try again.'
                return render(request, 'projects/verify_otp.html', {'error_message': error_message})
        else:
            error_message = 'Customer email not found. Please register again.'
            return render(request, 'projects/verify_otp.html', {'error_message': error_message})

    return render(request, 'projects/verify_otp.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            customeremail = form.cleaned_data['customeremail']
            customerpassword = form.cleaned_data['customerpassword']

            try:
                customer = Customer.objects.get(customeremail=customeremail)
                if check_password(customerpassword, customer.customerpassword):
                    session = Session(session_key=str(customer.id))
                    session.expire_date = timezone.now() + timedelta(days=7)  
                    session.save()
                    request.session['customer_id'] = customer.id
                    return redirect('project')  
                else:
                    messages.error(request, 'Invalid login credentials.')
            except Customer.DoesNotExist:
                messages.error(request, 'Invalid login credentials.')

    else:
        form = LoginForm()

    return render(request, 'projects/login.html', {'form': form})


def logout(request):
    if 'customer_id' in request.session:
        del request.session['customer_id']
    return redirect('project')  


