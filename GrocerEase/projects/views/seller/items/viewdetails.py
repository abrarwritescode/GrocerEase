from projects.imports import *

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def myitemdetails(request, pk, seller_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('home')   
    if 'seller_id' in request.session:
            seller_id = request.session['seller_id']
            seller = Seller.objects.get(pk=seller_id)
    itemObj = Item.objects.get(id=pk)
    categorys = itemObj.category.all() 
    return render(request, 'seller/singleitem.html', {'item':itemObj, 'categorys':categorys, 'seller': 'seller'})
