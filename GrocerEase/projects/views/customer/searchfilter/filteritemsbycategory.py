from projects.imports import *

def filteritemsbycategory(request, category_name, customer_id):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(pk=customer_id)
        data = cartData(request, customer_id)

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        products = Item.objects.all()
        categories = Category.objects.all()

    
        category = Category.objects.get(categoryname=category_name)
        items_in_category = Item.objects.filter(category=category)
        context = {
            'category': category,
            'items': items_in_category,
           
            'cartItems': cartItems,
            'customer': customer ,
            'categories': categories 
        }
        return render(request, 'customer/filteritemscategory.html', context)