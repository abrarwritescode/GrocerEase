from projects.imports import *

def filteritemsbyprice(request):
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 1000)  # Default values if not provided

    filtered_items = Item.objects.filter(itemprice__gte=min_price, itemprice__lte=max_price)

    return render(request, 'customer/filteritemsprice.html', {'items': filtered_items})
