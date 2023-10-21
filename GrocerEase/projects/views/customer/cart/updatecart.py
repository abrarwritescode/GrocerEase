from projects.imports import *

@csrf_exempt 
def updatecart(request):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('Action:', action)
        print('Product:', productId)

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'message': 'Customer not found'}, status=404)

        product = Item.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, is_cart=True)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
            seller = product.seller  
            added_datetime = timezone.now()  # Get the current date and time
            message = f"Your item '{product.itemtitle}' was added to a customer's cart by {customer.customername} at {added_datetime}."
            Notification.objects.create(sender=customer, recipient=seller, item=product, message=message)
            
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()
        

        



        return JsonResponse({'message': 'Item was added'}, safe=False)
    else:
        return JsonResponse({'message': 'Customer not authenticated'}, status=403)
    
