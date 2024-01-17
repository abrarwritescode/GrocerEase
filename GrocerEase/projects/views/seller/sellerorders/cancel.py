from django.shortcuts import get_object_or_404
from projects.imports import *

def cancel_order(request, seller_id):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        seller = get_object_or_404(Seller, id=seller_id)
        order_item = get_object_or_404(OrderItem, id=order_id, product__seller=seller)
        order_item.status = 'Cancelled'
        order_item.save()
