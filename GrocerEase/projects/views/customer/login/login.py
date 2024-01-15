from projects.imports import *
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logincustomer(request):
    if 'sessionid' in request.COOKIES:
        customer_id = request.session.get('customer_id', None)
        if customer_id is not None:
            return redirect('homecustomer', customer_id=customer_id)
    if request.method == 'POST':
        form = LoginCustomerForm(request.POST)
        if form.is_valid():
            customeremail = form.cleaned_data['customeremail']
            customerpassword = form.cleaned_data['customerpassword']

            try:
                customer = Customer.objects.get(customeremail=customeremail)
                if check_password(customerpassword, customer.customerpassword):
                    session = Session(session_key=str(customer.id))
                    session.expire_date = timezone.now() + timedelta(days=7)  
                    session.save()
                    request.session['customer_id'] = customer.id
                    request.session['customername'] = customer.customername

                    return redirect('homecustomer', customer_id=customer.id)
                else:
                    messages.error(request, 'Wrong password. Kindly try again.')

            except Customer.DoesNotExist:
                messages.error(request, 'Email does not exist.')

    else:
        form = LoginCustomerForm()

    return render(request, 'customer/logincustomer.html', {'form': form})
