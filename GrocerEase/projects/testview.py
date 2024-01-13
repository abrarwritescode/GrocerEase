from projects.imports import *

def vieworders(request, seller_id):
    seller_orders = OrderItem.objects.filter(
        product__seller_id=seller_id,
        order__status='Processing'
    ).select_related('product', 'order__customer')

    # You can further filter the orders if needed, for example, by date or any other criteria.

    context = {
        'seller_orders': seller_orders,
    }

    return render(request, 'orders.html', context)
