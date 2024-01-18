from projects.imports import *
from fuzzywuzzy import fuzz

def searchitems(request, customer_id):
    customer = None
    context = {}

    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(pk=customer_id)
        data = cartData(request, customer_id) 

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        products = Item.objects.all()
        categories = Category.objects.all()

    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
        
        products = Item.objects.all()
        

        relevant_items = [
            item for item in products
            if fuzz.partial_ratio(search_query.lower(), item.itemtitle.lower()) > 75
            or search_query.lower() in item.seller.storename.lower()

            or any(fuzz.partial_ratio(search_query.lower(), category.categoryname.lower()) > 75
                   for category in item.category.all())
        ]

        context = {
            'items': relevant_items,
            'search_query': search_query,
            'customer': customer,
            'cartItems': cartItems,
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            return render(request, 'customer/searchresult.html', context)

    return render(request, 'customer/search.html', context)
