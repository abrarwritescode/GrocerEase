from projects.imports import *

def logincustomer(request):
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
