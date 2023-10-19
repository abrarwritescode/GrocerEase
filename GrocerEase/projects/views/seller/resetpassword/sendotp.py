from projects.imports import *

def sendsellerresetotp(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                seller = Seller.objects.get(selleremail=email)

                
                otp = ''.join(random.choice('0123456789') for _ in range(6))
                seller.otp = otp
                seller.save()

                
                send_mail(
                    'GrocerEase Seller Password Reset OTP',
                    f'Your OTP for seller password reset is: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                
                return redirect('verify_reset_seller_otp', email=email)

            except Seller.DoesNotExist:
                
                pass
    else:
        form = PasswordResetForm()

    return render(request, 'projects/reset_seller_password.html', {'form': form})