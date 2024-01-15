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
        sellers = Seller.objects.all() 

        top_rated_items = (
        Item.objects
        .annotate(avg_rating=Avg('review__rating'))
        .filter(review__isnull=False)  
        .filter(avg_rating__gte=4.0) 
        .order_by('-avg_rating')[:8]
        )

        most_bought_items = customer.get_most_bought_items(num_items=2)
        print(1)
        print(2)
        print(most_bought_items)

        most_bought_items_by_count = customer.get_most_bought_items_by_count(num_items=2)
        print(1)
        print(2)
        print(most_bought_items_by_count)

        recently_viewed_item_ids = request.session.get('recently_viewed', [])
        recently_viewed_items = Item.objects.filter(id__in=recently_viewed_item_ids)

        recently_added_items = Item.objects.order_by('-uploadedon')[:8]  

        recently_viewed_categories = Item.objects.filter(id__in=recently_viewed_item_ids).values_list('category', flat=True)


        similar_items = Item.objects.filter(category__in=recently_viewed_categories).exclude(id__in=recently_viewed_item_ids).distinct()[:4]

        combined_items = recently_added_items | top_rated_items

        for item in recently_viewed_items:
            print(item.itemtitle)

        context = {
            'products': products,
            'cartItems': cartItems,
            'customer': customer_data ,
            'categories': categories ,
            'sellers': sellers,
            'recently_viewed_items': recently_viewed_items,
            'recently_added_items': recently_added_items,
            'similar_items': similar_items,
            'top_rated_items': top_rated_items,
            'combined_items': combined_items,
            'most_bought_items': most_bought_items,
            'most_bought_items_by_count': most_bought_items_by_count,
        }

        return render(request, 'customer/homecustomer.html', context)
    else:
        return redirect('logincustomer')
    

