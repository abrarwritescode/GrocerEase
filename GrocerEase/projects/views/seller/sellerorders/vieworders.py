from projects.imports import *
from django.shortcuts import render, redirect
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def vieworders(request, seller_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('home')
    
    if request.method == 'POST':
        order_item_id = request.POST.get('order_item_id')
        action = request.POST.get('action')
        action1 = request.POST.get('action1')

        if order_item_id and action == 'MARK_SHIPPED':
            order_item = OrderItem.objects.get(id=order_item_id)
            print(order_item)
            print(order_item.product)
            order_item.status = 'Shipped'
            order_item.save()

            order = order_item.order


            send_mail(
                    'GrocerEase Order Updates', 
                     f'Dear valued customer,\n\n'
                     f'Welcome to GrocerEase! '
                     'Your ordered item {order_item.product} is shipped to our warehouse successfully.\n\n'
                     f'Thank you for trusting GrocerEase.\n\n'
                     f'Best regards,\n'
                     f'The GrocerEase Team',
                    'grocereasedp1@gmail.com',
                    [order.shipping_email],
                    fail_silently=False,
                )


            order_items_to_update = OrderItem.objects.filter(order=order, product__seller_id=seller_id)
            order_items_to_update.update(status='Shipped')


        elif order_item_id and action1 == 'CANCEL':
            order_item = OrderItem.objects.get(id=order_item_id)
            order_item.status = 'Cancelled'
            order_item.save()

            order = order_item.order

            send_mail(
                    'GrocerEase Order Cancellation',
                    f'Dear valued customer,\n\n'
                    f'We regret to inform you that your ordered item {order_item.product} has been canceled.\n\n'
                    f'Thank you for considering GrocerEase.\n\n'
                    f'Best regards,\n'
                    f'The GrocerEase Team',
                    'grocereasedp1@gmail.com',
                    [order.shipping_email],
                    fail_silently=False,
)

            order_items_to_update = OrderItem.objects.filter(order=order, product__seller_id=seller_id)
            order_items_to_update.update(status='Cancelled')


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
