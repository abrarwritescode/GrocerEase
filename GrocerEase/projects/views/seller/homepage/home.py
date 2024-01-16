from projects.imports import *

@cache_control(no_cache=True, must_revalidate=True,no_store=True)

def homeseller(request, seller_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('loginseller')
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller = Seller.objects.get(pk=seller_id)
        items = Item.objects.filter(seller=seller) 
        context = {'items': items, 'seller':seller}
        return render(request, 'seller/homeseller.html', context)

    else:
        return redirect('loginseller') 