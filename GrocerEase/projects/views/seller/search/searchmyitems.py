from projects.imports import *

def sellersearch(request, seller_id):
    seller = Seller.objects.get(pk=seller_id)

    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
   

        items = Item.objects.filter(
        Q(seller=seller),
        Q(itemtitle__icontains=search_query) | Q(category__categoryname__icontains=search_query)
)


        context = {
            'items': items,
            'search_query': search_query,
            'seller': seller,
        }

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # This is an AJAX request, return the search results as HTML
            return render(request, 'seller/sellersearchresult.html', context)

        return render(request, 'seller/searchseller.html', context)
