from projects.imports import *

def non_logged_in_home(request):
    products = Item.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'guestuser/home.html', context)