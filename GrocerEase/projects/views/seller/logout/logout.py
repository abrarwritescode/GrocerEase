from projects.imports import *

def logoutseller(request):
    if 'seller_id' in request.session:
        del request.session['seller_id']
        request.session.flush()
    return redirect('home')  