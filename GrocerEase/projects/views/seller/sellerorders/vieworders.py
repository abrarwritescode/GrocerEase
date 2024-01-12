from projects.imports import *
from django.shortcuts import redirect

def vieworders(request, seller_id):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')

        if order_id and action in ['MARK_SHIPPED', 'ANOTHER_ACTION']:  
            order = Order.objects.get(id=order_id)

            if action == 'MARK_SHIPPED':
                order.status = 'Shipped'
                order.save()


    seller_orders = OrderItem.objects.filter(
    product__seller_id=seller_id,
    order__status__in=['Processing', 'Shipped', 'Delivered']
    ).select_related('product', 'order__customer')
 
    order = [order.order for order in seller_orders]

    context = {
        'seller_orders': seller_orders,
        'order': order,
    }

    return render(request, 'seller/orders.html', context)
