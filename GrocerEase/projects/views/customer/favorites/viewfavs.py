from projects.imports import *

def viewfavorites(request, customer_id):
   if 'customer_id' in request.session:
         customer_id = request.session['customer_id']
         customer = Customer.objects.get(pk=customer_id)

    # Get the current user's favorite items
         favorites = Favorite.objects.filter(customer=customer)
         cart_total = Order.objects.filter(customer=customer, is_cart=True).first().get_cart_items

         return render(request, 'customer/favorites.html', {'favorites': favorites, 'cart_total': cart_total})
