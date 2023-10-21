from projects.imports import *

def marknotificationsasread(request, seller_id):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        
        Notification.objects.filter(recipient=seller_id, is_read=False).update(is_read=True)

        return JsonResponse({"message": "Notifications marked as read"})
