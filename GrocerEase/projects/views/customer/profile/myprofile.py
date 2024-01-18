from projects.imports import *
from django.db.models import Count

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def customerprofile(request, customer_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('home')
    customer = Customer.objects.get(pk=customer_id)
    
    cart_total = Order.objects.filter(customer=customer, is_cart=True).first().get_cart_items

    orders = customer.order_set.all()

    for order in orders:
       
        status_counts = order.orderitem_set.values('status').annotate(count=Count('status'))

        if status_counts.filter(status='Cancelled', count=order.orderitem_set.count()).exists():
            order.status = 'Cancelled'
       
        elif status_counts.filter(status='Refunded', count=order.orderitem_set.count()).exists():
            order.status = 'Completed'

        elif status_counts.filter(status='Refunding In Progress', count=order.orderitem_set.count()).exists():
            order.status = 'Processing'
        
        

        order.save()        

    if request.method == 'POST':
        image_form = ChangeCustomerImageForm(request.POST, request.FILES, instance=customer)
        if image_form.is_valid():
            image_form.save()
            return redirect('customerprofile', customer_id=customer_id)

    else: 
        image_form = ChangeCustomerImageForm(instance=customer)
    


    context = {
        'customer': customer, 
        'image_form': image_form,
        'cart_total': cart_total
    }
    return render(request, 'customer/customerprofile.html', context)

def change_customer_image(request, customer_id):
    pass