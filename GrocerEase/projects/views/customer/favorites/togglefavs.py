# views.py
from projects.imports import *

def togglefavorite(request, pk, customer_id):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(pk=customer_id)
        item = Item.objects.get(id=pk)

        try:
            favorite = Favorite.objects.get(customer=customer, item=item)
            favorite.soft_delete()
            is_favorite = False
        except Favorite.DoesNotExist:
            Favorite.objects.create(customer=customer, item=item)
            is_favorite = True
            seller = item.seller
            notification_message = f"Your item { item.itemtitle } has been liked by { customer.customername }."
            Notification.objects.create(sender=customer, recipient=seller, message=notification_message)

        # Update the favorite count for the item
        item.favorite_count = Favorite.objects.filter(item=item).count()
        item.save()

       

        response_data = {
            'is_favorite': is_favorite,
            'favorite_count': item.favorite_count,
        }

        return JsonResponse(response_data)

    return JsonResponse({'is_favorite': False})