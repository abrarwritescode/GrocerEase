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
        complementary_items = order.get_complementary_items()
        context = {'items': items, 'order': order, 'cartItems': cartItems, 'customer': customer, 'complementary_items': complementary_items}
    else:
        context = {'items': [], 'order': {}, 'cartItems': 0, 'customer': None, 'complementary_items': []}

    return render(request, 'customer/cart.html', context)