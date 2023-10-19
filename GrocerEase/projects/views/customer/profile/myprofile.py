from projects.imports import *

def customerprofile(request, customer_id):
    customer_id = request.session.get('customer_id')
    customer = Customer.objects.get(pk=customer_id)
    return render(request, 'projects/customerprofile.html', {'customer': customer})