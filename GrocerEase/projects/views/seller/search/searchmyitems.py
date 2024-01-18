from projects.imports import *
from fuzzywuzzy import fuzz

def sellersearch(request, seller_id):
    seller = Seller.objects.get(pk=seller_id)

    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')


        all_items = Item.objects.filter(seller=seller)

        relevant_items = [
            item for item in all_items
            if fuzz.partial_ratio(search_query.lower(), item.itemtitle.lower()) > 70
            or any(fuzz.partial_ratio(search_query.lower(), category.categoryname.lower()) > 70
                   for category in item.category.all())
        ]

        context = {
            'items': relevant_items,
            'search_query': search_query,
            'seller': seller,
        }

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
          
            return render(request, 'seller/sellersearchresult.html', context)

        return render(request, 'seller/searchseller.html', context)
