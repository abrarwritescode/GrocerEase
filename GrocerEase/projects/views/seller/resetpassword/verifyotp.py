from projects.imports import *

def verifysellerresetotp(request, email):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '')
        seller = Seller.objects.get(selleremail=email)

        if entered_otp == seller.otp:
            return redirect('change_seller_password', email=email)
        else:
            error_message = 'Invalid OTP. Please try again.'
            return render(request, 'projects/verify_reset_seller_otp.html', {'error_message': error_message, 'email': email})

    return render(request, 'seller/verify_reset_seller_otp.html', {'email': email})