from projects.imports import *


def customerprofile(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)

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
    }
    return render(request, 'customer/customerprofile.html', context)

def change_customer_image(request, customer_id):
    pass