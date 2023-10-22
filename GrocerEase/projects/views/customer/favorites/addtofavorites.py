from projects.imports import *

def addtofavorites(request, pk, customer_id):
     if 'customer_id' in request.session:
         customer_id = request.session['customer_id']
         customer = Customer.objects.get(pk=customer_id)
         
         item = Item.objects.get(id=pk)
         # Check if the item is already in favorites
         favorite, created = Favorite.objects.get_or_create(customer=customer, item=item)

        

      
         
    
         return redirect('homecustomer', customer_id=customer_id)
