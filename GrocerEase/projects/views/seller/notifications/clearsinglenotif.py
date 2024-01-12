from projects.imports import *


def clearsinglenotif(request, notification_id, seller_id):
   
    if 'seller_id' not in request.session:
        return JsonResponse({"message": "Seller ID not set in the session"}, status=400)
    
    seller_id = request.session['seller_id']
    seller = get_object_or_404(Seller, pk=seller_id)

    notification = get_object_or_404(Notification, pk=notification_id)

    if notification.recipient != seller:
        return JsonResponse({"message": "You are not authorized to clear this notification"}, status=403)

    
    notification.delete() 
 

    return redirect('homeseller', seller_id=seller_id)

