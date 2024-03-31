from projects.imports import *

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def myitemdetails(request, pk, seller_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('home')    
    if 'seller_id' in request.session:
            seller_id = request.session['seller_id']
            seller = Seller.objects.get(pk=seller_id)
    itemObj = Item.objects.get(id=pk)
    total_reviews = Review.objects.filter(item=itemObj).count()
    average_rating = Review.objects.filter(item=itemObj).aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 2)
    stars = range(1, 6)

    reviews = Review.objects.filter(item=itemObj)
    categorys = itemObj.category.all() 
    return render(request, 'seller/singleitem.html', {'item':itemObj, 'categorys':categorys, 'seller': seller, 'total_reviews': total_reviews,  
        'average_rating': average_rating, 'stars': stars, 'reviews': reviews})
