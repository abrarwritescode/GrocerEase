import hashlib
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Customer, Seller, Item
from .forms import RegistrationCustomerForm, LoginCustomerForm, OTPVerificationCustomerForm, ItemForm, RegistrationSellerForm, LoginSellerForm, OTPVerificationSellerForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import HttpResponseForbidden
from datetime import timedelta
import re
from django.core.mail import send_mail
import random
from django.urls import reverse
from django.http import JsonResponse
import json
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings

# d
def registercustomer(request):
    if request.method == 'POST':
        form = RegistrationCustomerForm(request.POST)
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
                request.session['otp'] = otp

                send_mail(
                    'GrocerEase OTP Verification',
                     f'Dear valued customer,\n\n'
                     f'Thank you for choosing GrocerEase for your online shopping needs. To complete your account setup, '
                     f'we require you to verify your email address. Your OTP for account verification is: {otp}\n\n'
                     f'Please enter this code on our website to confirm your account and gain access to our services.\n\n'
                     f'Thank you for trusting GrocerEase.\n\n'
                     f'Best regards,\n'
                     f'The GrocerEase Team',
                    'grocereasedp1@gmail.com',
                    [user.customeremail],
                    fail_silently=False,
                )

                return redirect('verify_otpcustomer')
    else:
        form = RegistrationCustomerForm()

    return render(request, 'projects/signupcustomer.html', {'form': form})


# d
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
                return redirect('logincustomer')
            else:
                error_message = 'Invalid OTP. Please try again.'
                return render(request, 'projects/verify_otpcustomer.html', {'error_message': error_message})
        else:
            error_message = 'Customer email not found. Please register again.'
            return render(request, 'projects/verify_otpcustomer.html', {'error_message': error_message})

    return render(request, 'projects/verify_otpcustomer.html')

# d
def logincustomer(request):
    if request.method == 'POST':
        form = LoginCustomerForm(request.POST)
        if form.is_valid():
            customeremail = form.cleaned_data['customeremail']
            customerpassword = form.cleaned_data['customerpassword']

            try:
                customer = Customer.objects.get(customeremail=customeremail)
                if check_password(customerpassword, customer.customerpassword):
                    session = Session(session_key=str(customer.id))
                    session.expire_date = timezone.now() + timedelta(days=7)  
                    session.save()
                    request.session['customer_id'] = customer.id
                    request.session['customername'] = customer.customername

                    return redirect('homecustomer', customer_id=customer.id)
                else:
                    messages.error(request, 'Wrong password. Kindly try again.')

            except Customer.DoesNotExist:
                messages.error(request, 'Email does not exist.')

    else:
        form = LoginCustomerForm()

    return render(request, 'projects/logincustomer.html', {'form': form})

# d
def logoutcustomer(request):
    if 'customer_id' in request.session:
        del request.session['customer_id']
    return redirect('logincustomer')  

# d
def homecustomer(request, customer_id):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(pk=customer_id)
        data = cartData(request, customer_id)

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        customer_data = {
            'id': customer_id,
            'name': customer.customername,
        }

        products = Item.objects.all()
        categories = Category.objects.all()

        context = {
            'products': products,
            'cartItems': cartItems,
            'customer': customer_data ,
            'categories': categories 
        }

        return render(request, 'projects/homecustomer.html', context)
    else:
        return redirect('logincustomer')
    
# d
def customerprofile(request, customer_id):
    customer_id = request.session.get('customer_id')
    customer = Customer.objects.get(pk=customer_id)
    return render(request, 'projects/customerprofile.html', {'customer': customer})


# d
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

    return render(request, 'projects/signupseller.html', {'form': form})

# d
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
                return render(request, 'projects/verify_otpseller.html', {'error_message': error_message})
        else:
            error_message = 'Seller email not found. Please register again.'
            return render(request, 'projects/verify_otpseller.html', {'error_message': error_message})

    return render(request, 'projects/verify_otpseller.html')

# d
def loginseller(request):
    if request.method == 'POST':
        form = LoginSellerForm(request.POST)
        if form.is_valid():
            selleremail = form.cleaned_data['selleremail']
            sellerpassword = form.cleaned_data['sellerpassword']

            try:
                seller = Seller.objects.get(selleremail=selleremail)
                if check_password(sellerpassword, seller.sellerpassword):
                    session = Session(session_key=str(seller.id))
                    session.expire_date = timezone.now() + timedelta(days=7)  
                    session.save()
                    request.session['seller_id'] = seller.id
                    request.session['storename'] = seller.storename

                    return redirect('homeseller', seller_id=seller.id)
                else:
                    messages.error(request, 'Wrong password. Kindly try again.')
            except Seller.DoesNotExist:
                messages.error(request, 'Email does not exist.')

    else:
        form = LoginSellerForm()

    return render(request, 'projects/loginseller.html', {'form': form})

# d
def logoutseller(request):
    if 'seller_id' in request.session:
        del request.session['seller_id']
    return redirect('loginseller')  

# d
def homeseller(request, seller_id):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller = Seller.objects.get(pk=seller_id)
        items = Item.objects.filter(seller=seller) 
        context = {'items': items, 'seller':seller}
        return render(request, 'projects/homeseller.html', context)

    else:
        return redirect('loginseller') 

# d   
def sellerprofile(request, seller_id):
    seller_id = request.session.get('seller_id')
    seller = Seller.objects.get(pk=seller_id)
    return render(request, 'projects/sellerprofile.html', {'seller': seller})

# d
def uploadItem(request, seller_id):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller = Seller.objects.get(pk=seller_id)
        form = ItemForm()

        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                item = form.save(commit=False)
                item.seller = seller
                item.storename = seller.storename
                item.save()
                return redirect('homeseller', seller_id=seller_id)

        context = {'form': form, 'seller':seller}
        return render(request, 'projects/uploaditem.html', context)
    else:
        return redirect('loginseller')

# d
def updateItemSeller(request, pk):
    item = Item.objects.get(id=pk)
    form = ItemForm(instance=item)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if 'seller_id' in request.session:
            seller_id = request.session['seller_id']
            seller = Seller.objects.get(pk=seller_id)
            if form.is_valid():
                form.save()
                return redirect('homeseller', seller_id=seller_id)

    context = {'form': form, 'item': item}
    return render(request, 'projects/uploaditem.html', context)

# d
def deleteItem(request, pk):
    item = Item.objects.get(id=pk)

    if request.method == 'POST':
            if 'seller_id' in request.session:
                seller_id = request.session['seller_id']
                item.delete()
                return redirect('homeseller', seller_id=seller_id)

    context = {'object': item}
    return render(request, 'projects/deleteitem.html', context)

# d
def singleitem(request, pk):
    if 'seller_id' in request.session:
            seller_id = request.session['seller_id']
    itemObj = Item.objects.get(id=pk)
    categorys = itemObj.category.all() 
    return render(request, 'projects/singleitem.html', {'item':itemObj, 'categorys':categorys})

# d
def singleitemcustomer(request, pk):
    if 'customer_id' in request.session:
            customer_id = request.session['customer_id']
    itemObj = Item.objects.get(id=pk)
    categorys = itemObj.category.all() 
    return render(request, 'projects/singleitemcustomer.html', {'item':itemObj, 'categorys':categorys})

# d
def cart(request, customer_id=None):
    if customer_id is None:
        customer_id = request.session.get('customer_id')

    if customer_id is not None:
        customer = Customer.objects.get(pk=customer_id)
        data = cartData(request, customer_id)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        context = {'items': items, 'order': order, 'cartItems': cartItems, 'customer': customer}
    else:
        context = {'items': [], 'order': {}, 'cartItems': 0, 'customer': None}

    return render(request, 'projects/cart.html', context)

# d
def checkout(request, customer_id=None):
    if customer_id is None:
        customer_id = request.session.get('customer_id')

    items = []
    order = {}
    cartItems = 0
    customer = None

    if customer_id is not None:
        customer = Customer.objects.get(pk=customer_id)
        data = cartData(request, customer_id)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'customer': customer}

    return render(request, 'projects/checkout.html', context)

# d
@csrf_exempt
def updateItem(request):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('Action:', action)
        print('Product:', productId)

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'message': 'Customer not found'}, status=404)

        product = Item.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse({'message': 'Item was added'}, safe=False)
    else:
        return JsonResponse({'message': 'Customer not authenticated'}, status=403)
    

# d
def myItem(request, seller_id):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller = Seller.objects.get(pk=seller_id)
        items = Item.objects.filter(seller=seller) 
        context = {'items': items, 'seller': seller}
        return render(request, 'projects/myitem.html', context)
    else:
        return redirect('loginseller')

# d
def search(request, customer_id):
        if 'customer_id' in request.session:
            customer_id = request.session['customer_id']
            customer = Customer.objects.get(pk=customer_id)

        return render(request, 'projects/search.html')

def searchseller(request, seller_id):
        if 'seller_id' in request.session:
            seller_id = request.session['seller_id']
            seller = Seller.objects.get(pk=seller_id)

        return render(request, 'projects/searchseller.html')

# d
def viewshop(request, customer_id):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(pk=customer_id)
        data = cartData(request, customer_id)

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        customer_data = {
            'id': customer_id,
            'name': customer.customername,
        }

        products = Item.objects.all()
        categories = Category.objects.all()

        context = {
            'products': products,
            'cartItems': cartItems,
            'customer': customer_data ,
            'categories': categories 
        }

        return render(request, 'projects/shop.html', context)
    else:
        return redirect('logincustomer')

# d
def reset_password(request):
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

    return render(request, 'projects/reset_password.html', {'form': form})

# d
def verify_reset_otp(request, email):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '')
        customer = Customer.objects.get(customeremail=email)

        if entered_otp == customer.otp:
            return redirect('change_password', email=email)
        else:
            error_message = 'Invalid OTP. Please try again.'
            return render(request, 'projects/verify_reset_otp.html', {'error_message': error_message, 'email': email})

    return render(request, 'projects/verify_reset_otp.html', {'email': email})

# d
def change_password(request, email):
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
            return render(request, 'projects/change_password.html', {'error_messages': error_messages, 'email': email})

        customer.customerpassword = make_password(new_password)
        customer.otp = None
        customer.save()

        return redirect('logincustomer')

    return render(request, 'projects/change_password.html', {'email': email})

# d
def items(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')  # Correct the parameter name
        items = Item.objects.filter(itemtitle__icontains=search_query)
    
        context = {
            'items': items,
            'search_query': search_query,
        }
        
        return render(request, 'projects/search.html', context)



def reset_seller_password(request):
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

def verify_reset_seller_otp(request, email):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '')
        seller = Seller.objects.get(selleremail=email)

        if entered_otp == seller.otp:
            return redirect('change_seller_password', email=email)
        else:
            error_message = 'Invalid OTP. Please try again.'
            return render(request, 'projects/verify_reset_seller_otp.html', {'error_message': error_message, 'email': email})

    return render(request, 'projects/verify_reset_seller_otp.html', {'email': email})

def change_seller_password(request, email):
    seller = Seller.objects.get(selleremail=email)

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
            return render(request, 'projects/change_seller_password.html', {'error_messages': error_messages, 'email': email})
        seller.sellerpassword = make_password(new_password)
        seller.otp = None
        seller.save()
        return redirect('loginseller')

    return render(request, 'projects/change_seller_password.html', {'email': email})
