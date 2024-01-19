from projects.imports import *
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def filteritemsbyprice(request, customer_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('home')
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(pk=customer_id)

    min_price = request.GET.get('min_price', 0) 
    max_price = request.GET.get('max_price', 1000)  

    filtered_items = Item.objects.filter(itemprice__gte=min_price, itemprice__lte=max_price)
    
    
    context = {'items': filtered_items, 'customer': customer }
   
    return render(request, 'customer/filteritemsprice.html', context)
