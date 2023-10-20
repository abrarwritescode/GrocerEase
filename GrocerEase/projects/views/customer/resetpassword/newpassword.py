from projects.imports import *

def changecustomerpassword(request, email):
    customer = Customer.objects.get(customeremail=email)

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')

        digit_error = None
        special_char_error = None
        capital_error = None
        small_letter_error = None
        length_error = None

        if len(new_password) < 8:
            length_error = 'Password must be at least 8 characters long.'
        if not re.search(r'\d', new_password):
            digit_error = 'Password must contain at least one digit.'
        if not re.search(r'[A-Z]', new_password):
            capital_error = 'Password must contain at least one uppercase letter.'
        if not re.search(r'[a-z]', new_password):
            small_letter_error = 'Password must contain at least one lowercase letter.'
        if not re.search(r'[@#$%^&+=!]', new_password):
            special_char_error = 'Password must contain at least one special character.'

        if digit_error or special_char_error or capital_error or small_letter_error or length_error:
            error_messages = [message for message in [digit_error, special_char_error, capital_error, small_letter_error, length_error] if message]
            return render(request, 'customer/change_password.html', {'error_messages': error_messages, 'email': email})

        customer.customerpassword = make_password(new_password)
        customer.otp = None
        customer.save()

        return redirect('logincustomer')

    return render(request, 'customer/change_password.html', {'email': email})