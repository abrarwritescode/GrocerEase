from projects.imports import *

def verifycustomerresetotp(request, email):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '')
        customer = Customer.objects.get(customeremail=email)

        if entered_otp == customer.otp:
            return redirect('change_password', email=email)
        else:
            error_message = 'Invalid OTP. Please try again.'
            return render(request, 'projects/verify_reset_otp.html', {'error_message': error_message, 'email': email})

    return render(request, 'projects/verify_reset_otp.html', {'email': email})