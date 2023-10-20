from projects.imports import *

def sendcustomerresetotp(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                customer = Customer.objects.get(customeremail=email)

                
                otp = ''.join(random.choice('0123456789') for _ in range(6))
                customer.otp = otp
                customer.save()

                
                send_mail(
                    'GrocerEase Password Reset OTP',
                    f'Your OTP for password reset is: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

               
                return redirect('verify_reset_otp', email=email)

            except Customer.DoesNotExist:
                
                pass
    else:
        form = PasswordResetForm()

    return render(request, 'customer/reset_password.html', {'form': form})