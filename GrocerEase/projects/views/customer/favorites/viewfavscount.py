from projects.imports import *

def getfavoritescount(request, customer_id):
  if 'customer_id' in request.session:
         customer_id = request.session['customer_id']
         customer = Customer.objects.get(pk=customer_id)
         favorite_count = Favorite.objects.filter(customer=customer).count()
    

         response_data = {
         "favorite_count": favorite_count
          }

         return JsonResponse(response_data)
