from projects.imports import *

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

    return render(request, 'customer/cart.html', context)