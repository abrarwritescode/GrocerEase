from projects.imports import *

def verifyotpseller(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '')
        session_otp = request.session.get('otp', None)
        print(entered_otp, session_otp)

        user_email = request.session.get('registered_user_email', None)
        seller_name = request.session.get('registered_user_name', None)  
        seller_password = request.session.get('registered_user_password', None) 
        print(user_email, seller_name, seller_password)

        if user_email:
            if entered_otp == session_otp:
                user = Seller.objects.create(  # using Django's Object-Relational Mapping (ORM) instead of raw query
                    storename=seller_name,  
                    selleremail=user_email,
                    sellerpassword=seller_password,
                    otp=session_otp,  
                    is_verified=True
                )
                return redirect('loginseller')
            else:
                error_message = 'Invalid OTP. Please try again.'
                return render(request, 'seller/verify_otpseller.html', {'error_message': error_message})
        else:
            error_message = 'Seller email not found. Please register again.'
            return render(request, 'seller/verify_otpseller.html', {'error_message': error_message})

    return render(request, 'seller/verify_otpseller.html')
