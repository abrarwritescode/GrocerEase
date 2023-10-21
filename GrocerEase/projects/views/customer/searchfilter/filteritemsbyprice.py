from projects.imports import *

def filteritemsbyprice(request, customer_id):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(pk=customer_id)

    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 1000)  # Default values if not provided

    filtered_items = Item.objects.filter(itemprice__gte=min_price, itemprice__lte=max_price)
    
    template = loader.get_template('customer/filteritemsprice.html')  # Create a template for filtered results
    context = {'items': filtered_items, 'customer': customer }
    filtered_results = template.render(context)

    return HttpResponse(filtered_results)
