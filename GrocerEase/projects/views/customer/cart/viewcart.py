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
        
        # Get cart items
        cart_items = order.orderitem_set.filter(confirmed=False)

        itemObj = None
        recommended_items = []
        order_item = order.orderitem_set.filter(confirmed=False).first()

        if order_item:
            item_id = order_item.product.id
            itemObj = Item.objects.get(id=item_id)
            recommended_items = itemObj.get_recommendations(customer)

            # Filter out recommended items that are already in the cart
            cart_items_ids = [cart_item.product.id for cart_item in cart_items]
            recommended_items = [item for item in recommended_items if item.id not in cart_items_ids]

        context = {
            'items': items,
            'order': order,
            'cartItems': cartItems,
            'cart_items': cart_items,
            'customer': customer,
            'recommended_items': recommended_items,
        }
    else:
        context = {'items': [], 'order': {}, 'cartItems': 0, 'customer': None, 'complementary_items': []}

    return render(request, 'customer/cart.html', context)
