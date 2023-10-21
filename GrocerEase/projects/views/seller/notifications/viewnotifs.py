from projects.imports import *

def sellernotifs(request, seller_id):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller = Seller.objects.get(pk=seller_id)
        notifications = Notification.objects.filter(recipient=seller).order_by('-created_at')

    
    return render(request, 'seller/notifications.html', {'notifications': notifications})