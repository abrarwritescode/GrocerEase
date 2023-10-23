from projects.imports import *

def getnotificationcount(request, seller_id):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        unread_notification_count = Notification.objects.filter(
            recipient=seller_id, is_read=False
        ).count()

        return JsonResponse({"count": unread_notification_count, 'seller_id': seller_id})
    

 