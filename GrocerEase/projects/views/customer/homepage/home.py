from projects.imports import *

def homecustomer(request, customer_id):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(pk=customer_id)
        data = cartData(request, customer_id)

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        customer_data = {
            'id': customer_id,
            'name': customer.customername,
        }

        products = Item.objects.all()
        categories = Category.objects.all()

        context = {
            'products': products,
            'cartItems': cartItems,
            'customer': customer_data ,
            'categories': categories 
        }

        return render(request, 'customer/homecustomer.html', context)
    else:
        return redirect('logincustomer')
    
def non_logged_in_home(request):
    products = Item.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'customer/home.html', context)
