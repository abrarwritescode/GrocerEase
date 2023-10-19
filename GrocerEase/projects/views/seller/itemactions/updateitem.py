from projects.imports import *

def updateitem(request, pk):
    item = Item.objects.get(id=pk)
    form = ItemForm(instance=item)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if 'seller_id' in request.session:
            seller_id = request.session['seller_id']
            seller = Seller.objects.get(pk=seller_id)
            if form.is_valid():
                form.save()
                return redirect('homeseller', seller_id=seller_id)

    context = {'form': form, 'item': item}
    return render(request, 'projects/uploaditem.html', context)
