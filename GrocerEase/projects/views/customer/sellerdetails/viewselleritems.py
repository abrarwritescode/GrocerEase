from projects.imports import *

def selleritems(request, seller_id):
    seller = Seller.objects.get(pk=seller_id)
    items = Item.objects.filter(seller=seller)

    context = {
        'seller': seller,
        'items': items,
    }

    return render(request, 'seller/selleritems.html', context)