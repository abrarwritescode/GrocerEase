from projects.imports import *

def itemdetails(request, pk):
    if 'customer_id' in request.session:
            customer_id = request.session['customer_id']
    itemObj = Item.objects.get(id=pk)
    categorys = itemObj.category.all() 
    return render(request, 'customer/singleitemcustomer.html', {'item':itemObj, 'categorys':categorys})


