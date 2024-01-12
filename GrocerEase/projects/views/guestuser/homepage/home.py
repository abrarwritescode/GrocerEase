from projects.imports import *

def non_logged_in_home(request):
    products = Item.objects.all()
    categories = Category.objects.all()
    sellers = Seller.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'sellers': sellers
    }

    return render(request, 'guestuser/home.html', context)