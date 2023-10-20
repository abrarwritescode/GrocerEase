from projects.imports import *

def myitemdetails(request, pk):
    if 'seller_id' in request.session:
            seller_id = request.session['seller_id']
    itemObj = Item.objects.get(id=pk)
    categorys = itemObj.category.all() 
    return render(request, 'seller/singleitem.html', {'item':itemObj, 'categorys':categorys})
