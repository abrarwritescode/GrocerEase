from projects.imports import *

def guestselleritems(request, seller_id):

    products = Item.objects.all()
    categories = Category.objects.all()
    seller = Seller.objects.get(pk=seller_id)
    items = Item.objects.filter(seller=seller)
    
    context = {
        'seller': seller,
        'items': items,
        'products': products,
        'categories': categories 
    }

    return render(request, 'guestuser/guestselleritems.html', context)