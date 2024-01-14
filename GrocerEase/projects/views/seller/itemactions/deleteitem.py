from projects.imports import *

def deleteitem(request, pk):
    item = Item.objects.get(id=pk)

    if request.method == 'POST':
            if 'seller_id' in request.session:
                seller_id = request.session['seller_id']
                item.soft_delete()
                return redirect('homeseller', seller_id=seller_id)

    context = {'object': item}
    return render(request, 'seller/deleteitem.html', context)