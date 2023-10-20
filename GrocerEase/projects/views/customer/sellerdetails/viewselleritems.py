from projects.imports import *

def selleritems(request, seller_id, customer_id):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(pk=customer_id)
        data = cartData(request, customer_id)

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

       
        products = Item.objects.all()
        categories = Category.objects.all()


    seller = Seller.objects.get(pk=seller_id)
    items = Item.objects.filter(seller=seller)

    context = {
        'seller': seller,
        'items': items,
        'products': products,
        'cartItems': cartItems,
        'customer': customer ,
        'categories': categories 
    }

    return render(request, 'seller/selleritems.html', context)