from projects.imports import *

def itemdetails(request, pk, customer_id):
    if 'customer_id' in request.session:
            customer_id = request.session['customer_id']
            customer = Customer.objects.get(pk=customer_id)
            data = cartData(request, customer_id)

            
            cartItems = data['cartItems']
            order = data['order']
            items = data['items']

            products = Item.objects.all()
            categories = Category.objects.all() 

    itemObj = Item.objects.get(id=pk)
    categorys = itemObj.category.all() 
    return render(request, 'customer/singleitemcustomer.html', {'item':itemObj, 'categorys':categorys,  'products': products,
            'cartItems': cartItems,
            'customer': customer ,
            'categories': categories })


