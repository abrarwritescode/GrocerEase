from projects.imports import *

def filteritemsbycategory(request, category_name):
    
        category = Category.objects.get(categoryname=category_name)
        items_in_category = Item.objects.filter(category=category)
        context = {
            'category': category,
            'items': items_in_category,
        }
        return render(request, 'customer/categoryitems.html', context)