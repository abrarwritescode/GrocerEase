from projects.imports import *
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def myitems(request, seller_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('home')   
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller = Seller.objects.get(pk=seller_id)
        items = Item.objects.filter(seller=seller) 
        context = {'items': items, 'seller': seller}
        return render(request, 'seller/myitem.html', context)
    else:
        return redirect('loginseller')