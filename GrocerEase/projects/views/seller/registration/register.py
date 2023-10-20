from projects.imports import *

def registerseller(request):
    if request.method == 'POST':
        form = RegistrationSellerForm(request.POST)

        if form.is_valid():
            
            password = form.cleaned_data['sellerpassword']
            

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
                    form.add_error('sellerpassword', digit_error)
                if special_char_error:
                    form.add_error('sellerpassword', special_char_error)
                if capital_error:
                    form.add_error('sellerpassword', capital_error)
                if small_letter_error:
                    form.add_error('sellerpassword', small_letter_error)
                if length_error:
                    form.add_error('sellerpassword', length_error)
                print("Password validation failed")
            else:
                user = form.save(commit=False)  # user object in memory
                user.sellerpassword = make_password(password)  # password hash
                otp = ''.join(random.choice('0123456789') for _ in range(6))
                user.otp = otp

                request.session['registered_user_email'] = user.selleremail
                request.session['registered_user_name'] = user.storename
                request.session['registered_user_password'] = user.sellerpassword
                request.session['otp'] = otp

                send_mail(
                    'GrocerEase OTP Verification',
                     f'Dear valued seller,\n\n'
                     f'Thank you for choosing GrocerEase for your online shopping needs. To complete your account setup, '
                     f'we require you to verify your email address. Your OTP for account verification is: {otp}\n\n'
                     f'Please enter this code on our website to confirm your account and gain access to our services.\n\n'
                     f'Thank you for trusting GrocerEase.\n\n'
                     f'Best regards,\n'
                     f'The GrocerEase Team',
                    'grocereasedp1@gmail.com',
                    [user.selleremail],
                    fail_silently=False,
                )

                return redirect('verify_otpseller')  
        
           

    else:
        form = RegistrationSellerForm()

    return render(request, 'seller/signupseller.html', {'form': form})