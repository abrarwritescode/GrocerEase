from projects.imports import *
from decimal import Decimal

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

        amount_in_smallest_unit = order.get_cart_total * 100

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'customer': customer, 'amount_in_cents': amount_in_smallest_unit}

    if request.method == 'POST':
        shipping_name = request.POST.get('name')
        shipping_email = request.POST.get('email')
        shipping_address = request.POST.get('address')
        shipping_phone = request.POST.get('phone') 
        payment_method = request.POST.get('payment_method')  # Add this line to get the payment method

        order.shipping_name = shipping_name
        order.shipping_email = shipping_email
        order.shipping_address = shipping_address
        order.shipping_phone = shipping_phone
        order.status = 'Processing'  
        order.payment = Decimal(order.get_cart_total)
        order.payment_method = payment_method

        if order.payment_method == 'Cash on Delivery':
            order.is_cart = False
            print( order.shipping_name)
            order.save()

            send_mail(
                'GrocerEase Order Confirmation', 
                f'Dear valued customer,\n\n'
                f'Welcome to GrocerEase! '
                'Your order is placed successfully.\n\n'
                f'Your payable amount is BDT { order.payment } for order ID: { order.id } is to be paid during delivery.\n\n'
                f'Thank you for trusting GrocerEase.\n\n'
                f'Best regards,\n'
                f'The GrocerEase Team',
                'grocereasedp1@gmail.com',
                [order.shipping_email],
                fail_silently=False,
            )
            messages.success(request, 'Order placed successfully!')
            return redirect('homecustomer', customer_id=customer_id)
        else:
            try:
                token = request.POST['stripeToken']

                print(f"Order object: {order}")
                if order:
                    order.is_cart = False
                    order.save()

                    send_mail(
                        'GrocerEase Order Confirmation', 
                         f'Dear valued customer,\n\n'
                         f'Welcome to GrocerEase! '
                         'Your order is placed successfully.\n\n'
                         f'Your payable amount BDT {order.payment} for order ID: {order.id} is successful.\n\n'
                         f'Thank you for trusting GrocerEase.\n\n'
                         f'Best regards,\n'
                         f'The GrocerEase Team',
                        'grocereasedp1@gmail.com',
                        [order.shipping_email],
                        fail_silently=False,
                    )

                messages.success(request, 'Order placed successfully!')
                return redirect('homecustomer', customer_id=customer_id)

            except Exception as e:
                messages.error(request, str(e))

    return render(request, 'customer/checkout.html', context)