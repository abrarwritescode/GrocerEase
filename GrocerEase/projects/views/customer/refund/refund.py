from projects.imports import *

def refund(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)

    order_item.status = 'Refunding In Progress'
    order_item.save()

    refund_amount = order_item.product.itemprice * order_item.quantity

    Refund.objects.create(
        order_item=order_item,
        customer=order_item.order.customer,
        refund_amount=refund_amount,
    )

    customer_id = order_item.order.customer.id

    send_mail(
        'GrocerEase Refund Process in Progress',
        f'Dear valued customer,\n\n'
        f'We have received your request for a refund, and the process is now in progress.\n\n'
        f'Your refundable amount for order item { order_item.product.itemtitle } from { order_item.product.seller } is BDT { refund_amount }.\n\n'
        f'Thank you for choosing GrocerEase.\n\n'
        f'Best regards,\n'
        f'The GrocerEase Team',
        'grocereasedp1@gmail.com',
        [order_item.order.shipping_email], 
        fail_silently=False,
    )

    messages.success(request, 'Refund process initiated successfully.')
    return redirect('customerprofile', customer_id=customer_id)
