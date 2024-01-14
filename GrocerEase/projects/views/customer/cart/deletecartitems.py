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

            order_item.delete()

            
            return JsonResponse({'message': 'Item removed from the cart and stock updated'}, status=200)
        except OrderItem.DoesNotExist:
            return JsonResponse({'message': 'Item not found in the cart'}, status=404)
    return JsonResponse({'message': 'Invalid request method'}, status=400)

