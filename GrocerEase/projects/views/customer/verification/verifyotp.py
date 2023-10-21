from projects.imports import *
from django.urls import reverse
from django.http import HttpResponseRedirect

def verifyotpcustomer(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '')
        session_otp = request.session.get('otp', None)
        print(entered_otp, session_otp)

        user_email = request.session.get('registered_user_email', None)
        customer_name = request.session.get('registered_user_name', None)  
        customer_password = request.session.get('registered_user_password', None) 
        print(user_email, customer_name, customer_password)

        if user_email:
            if entered_otp == session_otp:
                user = Customer.objects.create(  # using Django's Object-Relational Mapping (ORM) instead of raw query
                    customername=customer_name,  
                    customeremail=user_email,
                    customerpassword=customer_password,
                    otp=session_otp,  
                    is_verified=True
                )
                return HttpResponseRedirect(reverse('logincustomer') + '#login-section')
            else:
                error_message = 'Invalid OTP. Please try again.'
                return render(request, 'customer/verify_otpcustomer.html', {'error_message': error_message})
        else:
            error_message = 'Customer email not found. Please register again.'
            return render(request, 'customer/verify_otpcustomer.html', {'error_message': error_message})

    return render(request, 'customer/verify_otpcustomer.html')