from projects.imports import *

def sellerprofile(request, seller_id):
    seller_id = request.session.get('seller_id')
    seller = Seller.objects.get(pk=seller_id)

    if request.method == 'POST':
        form = EditSellerForm(request.POST, instance=seller)  # Use your EditSellerForm

        if form.is_valid():
            form.save()  # Save the edited seller information
            return redirect('sellerprofile', seller_id=seller.id)  # Redirect to the seller profile page or another appropriate URL after editing

    else:
        form = EditSellerForm(instance=seller)  # Prefill the form with the seller's current information

    return render(request, 'seller/sellerprofile.html', {'seller': seller, 'form': form})
