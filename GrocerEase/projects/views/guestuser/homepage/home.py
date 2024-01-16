from projects.imports import *

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def non_logged_in_home(request):
    if 'sessionid' in request.COOKIES:
        customer_id = request.session.get('customer_id', None)
        if customer_id is not None:
            return redirect('homecustomer', customer_id=customer_id)
    if 'sessionid' in request.COOKIES:
        seller_id = request.session.get('seller_id', None)
        if seller_id is not None:
            return redirect('homeseller', seller_id=seller_id)   
    products = Item.objects.all()
    categories = Category.objects.all()
    sellers = Seller.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'sellers': sellers
    }

    return render(request, 'guestuser/home.html', context)