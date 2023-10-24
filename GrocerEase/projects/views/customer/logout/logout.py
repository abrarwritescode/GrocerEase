from projects.imports import *

def logoutcustomer(request):
    if 'customer_id' in request.session:
        del request.session['customer_id']
    return redirect('home')  