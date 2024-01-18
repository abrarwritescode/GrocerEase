from projects.imports import *
from django.shortcuts import render, redirect
from django.db.models import Q

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def vieworders(request, seller_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('home')
    
    if request.method == 'POST':
        order_item_id = request.POST.get('order_item_id')
        order_item_id1 = request.POST.get('order_item_id1')
        action = request.POST.get('action')
        action1 = request.POST.get('action1')

        if order_item_id and action == 'MARK_SHIPPED':
            order_item = OrderItem.objects.get(id=order_item_id)
            order_item.status = 'Shipped'
            order_item.save()
            print(order_item.product)

            order = order_item.order

        elif order_item_id1 and action1 == 'CANCEL':
            order_item = OrderItem.objects.get(id=order_item_id1)
            order_item.status = 'Cancelled'
            order_item.save()
            print(order_item.product)

            order = order_item.order

            send_mail(
                    'GrocerEase Order Cancellation',
                    f'Dear valued customer,\n\n'
                    f'We regret to inform you that your ordered item {order_item.product} from { order_item.product.seller } has been canceled.\n\n'
                    f'Thank you for considering GrocerEase.\n\n'
                    f'Best regards,\n'
                    f'The GrocerEase Team',
                    'grocereasedp1@gmail.com',
                    [order.shipping_email],
                    fail_silently=False,
)


    seller_orders = OrderItem.objects.filter(
        product__seller_id=seller_id,
        order__status__in=['Processing', 'Shipped', 'Delivered', 'Cancelled']
    ).select_related('product', 'order__customer')

    order_data = {}
    for order_item in seller_orders:
        order_id = order_item.order.id
        if order_id not in order_data:
            order_data[order_id] = {'order': order_item.order, 'items': []}

        order_data[order_id]['items'].append(order_item)

    orders_info = list(order_data.values())

    context = {
        'orders_info': orders_info,
    }

    return render(request, 'seller/orders.html', context)
