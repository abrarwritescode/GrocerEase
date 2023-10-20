from projects.imports import *

def sellerprofile(request, seller_id):
    seller_id = request.session.get('seller_id')
    seller = Seller.objects.get(pk=seller_id)
    return render(request, 'seller/sellerprofile.html', {'seller': seller})
