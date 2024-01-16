from projects.imports import *
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def uploaditem(request, seller_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('home')   
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller = Seller.objects.get(pk=seller_id)  
        form = ItemForm()

        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                item = form.save(commit=False)
                item.seller = seller 
                item.storename = seller.storename

                if item.discount_percentage > 0:
                    discount_amount = (item.discount_percentage / 100) * item.original_price
                    item.itemprice = item.original_price
                    item.discounted_price = item.itemprice - discount_amount
                    item.itemprice=item.discounted_price
                else:
                    item.discounted_price = item.original_price
                    item.itemprice = item.original_price
                
                item.save()

                for category in form.cleaned_data['category']:
                    item.category.add(category)
                return redirect('homeseller', seller_id=seller_id)

        context = {'form': form, 'seller': seller}
        return render(request, 'seller/uploaditem.html', context)
    else:
        return redirect('loginseller')
