from projects.imports import *

def homeseller(request, seller_id):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller = Seller.objects.get(pk=seller_id)
        items = Item.objects.filter(seller=seller) 
        context = {'items': items, 'seller':seller}
        return render(request, 'projects/homeseller.html', context)

    else:
        return redirect('loginseller') 