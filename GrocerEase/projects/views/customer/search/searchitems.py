from projects.imports import *

def searchitems(request, customer_id):
    customer = None

    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(pk=customer_id)

    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
        items = Item.objects.filter(itemtitle__iexact=search_query)


        context = {
            'items': items,
            'search_query': search_query,
            'customer': customer,
        }

        return render(request, 'projects/search.html', context)

  
