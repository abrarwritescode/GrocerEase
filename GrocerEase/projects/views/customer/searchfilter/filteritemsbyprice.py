from projects.imports import *

def filteritemsbyprice(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    # Filter items based on price range
    filtered_items = Item.objects.filter(itemprice__gte=min_price, itemprice__lte=max_price)

    return render(request, 'customer/filteritemsprice.html', {'items': filtered_items})