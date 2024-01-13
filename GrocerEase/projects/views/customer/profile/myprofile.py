from projects.imports import *


def customerprofile(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    
    cart_total = Order.objects.filter(customer=customer, is_cart=True).first().get_cart_items

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