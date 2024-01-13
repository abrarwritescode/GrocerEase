from projects.imports import *

@csrf_exempt
def delete_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            order_item = OrderItem.objects.get(id=item_id)
            product = order_item.product
            quantity = order_item.quantity

            product.itemquantity += quantity
            product.save()

            customer = order_item.order.customer
            seller = product.seller
            added_datetime = timezone.now()
            current_datetime = added_datetime + timedelta(hours=6)
            message = f"Your item '{product.itemtitle}' was entirely removed from customer: {customer.customername}'s cart at {current_datetime}. Current Quantity of {product.itemtitle}: {product.itemquantity}."
            Notification.objects.create(sender=customer, recipient=seller, item=product, message=message)

            order_item.delete()

            
            return JsonResponse({'message': 'Item removed from the cart and stock updated'}, status=200)
        except OrderItem.DoesNotExist:
            return JsonResponse({'message': 'Item not found in the cart'}, status=404)
    return JsonResponse({'message': 'Invalid request method'}, status=400)

