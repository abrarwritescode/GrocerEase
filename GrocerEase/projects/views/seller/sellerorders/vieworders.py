from projects.imports import *
from django.shortcuts import render, redirect
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def vieworders(request, seller_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('home')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        action1 = request.POST.get('action1')

        if order_id and action == 'MARK_SHIPPED':
            order = Order.objects.get(id=order_id)
            order.status = 'Shipped'
            order.save()

        elif order_id and action1 == 'CANCEL':
            order = Order.objects.get(id=order_id)
            order.status = 'Cancelled'
            order.save()

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
