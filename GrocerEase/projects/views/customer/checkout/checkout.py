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

        order.shipping_name = shipping_name
        order.shipping_email = shipping_email
        order.shipping_address = shipping_address
        order.shipping_phone = shipping_phone
        order.status = 'Processing'  
        order.payment = Decimal(order.get_cart_total)


        try:
            token = request.POST['stripeToken']

            order.save()

            order_items = order.orderitem_set.all()
            order_items.delete()

            messages.success(request, 'Order placed successfully!')
            return redirect('homecustomer', customer_id=customer_id)

        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'customer/checkout.html', context)
