def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['customerpassword']

            if not re.match(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$%^&+=!]).{8,}$', password):
                form.add_error('customerpassword', 'Password must contain at least one digit, one uppercase letter, one lowercase letter, and one special character.')
                print("Password regex validation failed")
            else:
                try:
                    validate_password(password)
                except ValidationError as e:
                    form.add_error('customerpassword', e.messages[0])
                    print(f"Password validation failed: {e.messages[0]}")
                else:
                    user = form.save(commit=False)  # user object in memory
                    user.customerpassword = make_password(password)  # password hash

                    # Generate OTP (e.g., 6 digits)
                    otp = ''.join(random.choice('0123456789') for _ in range(6))
                    user.otp = otp
                    user.save()

                    # Send OTP to the user's email (you'll need to set up email settings)
                    send_mail(
                        'OTP Verification',
                        f'Your OTP for account verification is: {otp}',
                        'your@email.com',  # Replace with your email address
                        [user.customeremail],
                        fail_silently=False,
                    )

                    return redirect('verify_otp')  # Redirect to OTP verification page

    else:
        form = RegistrationForm()

    return render(request, 'projects/signup.html', {'form': form})
