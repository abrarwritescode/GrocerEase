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


def registercustomer(request):
    if request.method == 'POST':
        form = RegistrationCustomerForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['customerpassword']

            if not re.match(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$%^&+=!]).{8,}$', password):
                form.add_error('customerpassword', 'Password must contain at least one digit, one uppercase letter, one lowercase letter, and one special character.')
                print("Password regex validation failed")

            try:
                validate_password(password)
            except ValidationError as e:
                form.add_error('customerpassword', e.messages[0])
                print(f"Password validation failed: {e.messages[0]}")
            else:
                user = form.save(commit=False)  # user object in memory
                user.customerpassword = make_password(password)  # password hash
                otp = ''.join(random.choice('0123456789') for _ in range(6))
                user.otp = otp

                request.session['registered_user_email'] = user.customeremail
                request.session['registered_user_name'] = user.customername
                request.session['registered_user_password'] = user.customerpassword
                request.session['otp'] = otp

                send_mail(
                    'GrocerEase OTP Verification',
                    f'Dear customer, your OTP for account verification is: {otp}',
                    'grocereasedp1@gmail.com',
                    [user.customeremail],
                    fail_silently=False,
                )

                return redirect('verify_otpcustomer')  

    else:
        form = RegistrationCustomerForm()

    return render(request, 'projects/signupcustomer.html', {'form': form})


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
                    return redirect('homecustomer', customer_id=customer.id)
                else:
                    messages.error(request, 'Invalid login credentials.')

            except Customer.DoesNotExist:
                messages.error(request, 'Invalid login credentials.')

    else:
        form = LoginCustomerForm()

    return render(request, 'projects/logincustomer.html', {'form': form})


def logoutcustomer(request):
    if 'customer_id' in request.session:
        del request.session['customer_id']
    return redirect('logincustomer')  


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
        context = {
            'products': products,
            'cartItems': cartItems,
            'customer': customer_data  
        }

        return render(request, 'projects/homecustomer.html', context)
    else:
        return redirect('logincustomer')



def registerseller(request):
    if request.method == 'POST':
        form = RegistrationSellerForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['sellerpassword']

            if not re.match(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$%^&+=!]).{8,}$', password):
                form.add_error('sellerpassword', 'Password must contain at least one digit, one uppercase letter, one lowercase letter, and one special character.')
                print("Password regex validation failed")

            try:
                validate_password(password)
            except ValidationError as e:
                form.add_error('sellerpassword', e.messages[0])
                print(f"Password validation failed: {e.messages[0]}")
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
                    f'Dear seller, your OTP for account verification is: {otp}',
                    'grocereasedp1@gmail.com',
                    [user.selleremail],
                    fail_silently=False,
                )

                return redirect('verify_otpseller')  

    else:
        form = RegistrationSellerForm()

    return render(request, 'projects/signupseller.html', {'form': form})


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
                    return redirect('homeseller', seller_id=seller.id)
                else:
                    messages.error(request, 'Invalid login credentials.')
            except Seller.DoesNotExist:
                messages.error(request, 'Invalid login credentials.')

    else:
        form = LoginSellerForm()

    return render(request, 'projects/loginseller.html', {'form': form})


def logoutseller(request):
    if 'seller_id' in request.session:
        del request.session['seller_id']
    return redirect('loginseller')  


def homeseller(request, seller_id):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller = Seller.objects.get(pk=seller_id)
        items = Item.objects.all() 
        context = {'items': items, 'seller':seller}
        return render(request, 'projects/homeseller.html', context)

    else:
        return redirect('loginseller') 


def uploadItem(request):
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

        context = {'form': form}
        return render(request, 'projects/uploaditem.html', context)
    else:
        return redirect('loginseller')


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


def deleteItem(request, pk):
    item = Item.objects.get(id=pk)

    if request.method == 'POST':
            if 'seller_id' in request.session:
                seller_id = request.session['seller_id']
                item.delete()
                return redirect('homeseller', seller_id=seller_id)

    context = {'object': item}
    return render(request, 'projects/deleteitem.html', context)

    
def singleitem(request, pk):
    if 'seller_id' in request.session:
            seller_id = request.session['seller_id']
    itemObj = Item.objects.get(id=pk)
    return render(request, 'projects/singleitem.html', {'item':itemObj})


def singleitemcustomer(request, pk):
    if 'customer_id' in request.session:
            customer_id = request.session['customer_id']
    itemObj = Item.objects.get(id=pk)
    return render(request, 'projects/singleitemcustomer.html', {'item':itemObj})


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
    

def myItem(request, seller_id):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller = Seller.objects.get(pk=seller_id)
        items = Item.objects.filter(seller=seller) 
        context = {'items': items, 'seller': seller}
        return render(request, 'projects/myitem.html', context)
    else:
        return redirect('loginseller')
