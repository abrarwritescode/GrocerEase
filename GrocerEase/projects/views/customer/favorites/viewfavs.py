from projects.imports import *
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewfavorites(request, customer_id):
   if 'sessionid' not in request.COOKIES:
        return redirect('home')

   if 'customer_id' in request.session:
         customer_id = request.session['customer_id']
         customer = Customer.objects.get(pk=customer_id)

    # Get the current user's favorite items
         favorites = Favorite.objects.filter(customer=customer)
         cart_total = Order.objects.filter(customer=customer, is_cart=True).first().get_cart_items

         return render(request, 'customer/favorites.html', {'items': favorites, 'cart_total': cart_total, 'customer': customer})
