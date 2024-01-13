from projects.imports import *

def registercustomer(request):
    if request.method == 'POST':
        form = RegistrationCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            password = form.cleaned_data['customerpassword']

            digit_error = None
            special_char_error = None
            capital_error = None
            small_letter_error = None
            length_error = None

            if len(password) < 8:
                length_error = 'Password must be at least 8 characters long.'
            if not re.search(r'\d', password):
                digit_error = 'Password must contain at least one digit.'
            if not re.search(r'[A-Z]', password):
                capital_error = 'Password must contain at least one uppercase letter.'
            if not re.search(r'[a-z]', password):
                small_letter_error = 'Password must contain at least one lowercase letter.'
            if not re.search(r'[@#$%^&+=!]', password):
                special_char_error = 'Password must contain at least one special character.'

            if digit_error or special_char_error or capital_error or small_letter_error or length_error:
                if digit_error:
                    form.add_error('customerpassword', digit_error)
                if special_char_error:
                    form.add_error('customerpassword', special_char_error)
                if capital_error:
                    form.add_error('customerpassword', capital_error)
                if small_letter_error:
                    form.add_error('customerpassword', small_letter_error)
                if length_error:
                    form.add_error('customerpassword', length_error)
                print("Password validation failed")
            else:
                user = form.save(commit=False)
                user.customerpassword = make_password(password)
                otp = ''.join(random.choice('0123456789') for _ in range(6))
                user.otp = otp

                request.session['registered_user_email'] = user.customeremail
                request.session['registered_user_name'] = user.customername
                request.session['registered_user_password'] = user.customerpassword
                request.session['registered_user_image'] = user.customerimage.name
                request.session['otp'] = otp

                send_mail(
                    'GrocerEase OTP Verification', 
                     f'Dear valued customer,\n\n'
                     f'Welcome to GrocerEase! To complete your account setup, '
                     'we require you to verify your email address.\n\n'
                     f'Your OTP for account verification is: {otp}\n\n'
                     f'Please enter this code on our website to confirm your account and gain access to our services.\n\n'
                     f'Thank you for trusting GrocerEase.\n\n'
                     f'Best regards,\n'
                     f'The GrocerEase Team',
                    'grocereasedp1@gmail.com',
                    [user.customeremail],
                    fail_silently=False,
                )

                return HttpResponseRedirect(reverse('verify_otpcustomer') + '#verify-otp')
    else:
        form = RegistrationCustomerForm()

    return render(request, 'customer/signupcustomer.html', {'form': form})