from projects.imports import *




def removefromfavorites(request, pk, customer_id):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(pk=customer_id)
        item = Item.objects.get(id=pk)
        # Remove the item from favorites if it exists
        Favorite.objects.filter(customer=customer, item=item).delete()

       
        return redirect('homecustomer', customer_id=customer_id)
