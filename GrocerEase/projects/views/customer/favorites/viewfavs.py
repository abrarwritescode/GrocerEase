from projects.imports import *

def viewfavorites(request, customer_id):
   if 'customer_id' in request.session:
         customer_id = request.session['customer_id']
         customer = Customer.objects.get(pk=customer_id)

    # Get the current user's favorite items
         favorites = Favorite.objects.filter(customer=customer)

         return render(request, 'customer/favorites.html', {'favorites': favorites})
