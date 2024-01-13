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
                item = form.save(commit=False)
                
                if item.discount_percentage > 0:
                    discount_amount = (item.discount_percentage / 100) * item.original_price
                    item.itemprice = item.original_price
                    item.discounted_price = item.itemprice - discount_amount
                    item.itemprice=item.discounted_price
                else:
                    item.discounted_price = item.original_price
                    item.itemprice = item.original_price
                
                item.save()

                return redirect('homeseller', seller_id=seller_id)

    context = {'form': form, 'item': item}
    return render(request, 'seller/uploaditem.html', context)
