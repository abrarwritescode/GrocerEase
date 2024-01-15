from projects.imports import *
from projects.recommendation_utils import generate_item_features, calculate_similarity, get_recommendations

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def personalgrocerylist(request, customer_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('home')   

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

        all_items = list(Item.objects.all())
        customer_favorites = list(Favorite.objects.filter(customer=customer))

        customer_item_features = generate_item_features(all_items)
        customer_similarity_matrix = calculate_similarity(customer_item_features)

        fav_recommendations_list = []

        for favorite_item in customer_favorites:
            # index of the favorite item within the list of items
            item_index = all_items.index(favorite_item.item)

            recommendations = get_recommendations(item_index, all_items, customer_similarity_matrix)

            fav_recommendations_list.extend(recommendations)

        products = Item.objects.all()
        categories = Category.objects.all()
        sellers = Seller.objects.all() 

        all_items = list(Item.objects.all())
        customer_favorites = list(Favorite.objects.filter(customer=customer))

        customer_item_features = generate_item_features(all_items)
        customer_similarity_matrix = calculate_similarity(customer_item_features)

        fav_recommendations_list = []
        similar_items1 = []

        for favorite_item in customer_favorites:
            # index of the favorite item within the list of items
            item_index = all_items.index(favorite_item.item)

            recommendations = get_recommendations(item_index, all_items, customer_similarity_matrix)

            fav_recommendations_list.extend(recommendations)
        print(2)
        print(fav_recommendations_list)
        fav_recommendations_ids = [item.id for item in fav_recommendations_list]
        fav_recommendations_queryset = Item.objects.filter(id__in=fav_recommendations_ids)


        recently_viewed_item_ids = request.session.get('recently_viewed', [])
        recently_viewed_items = Item.objects.filter(id__in=recently_viewed_item_ids)

        recently_viewed_categories = Item.objects.filter(id__in=recently_viewed_item_ids).values_list('category', flat=True)


        similar_items = Item.objects.filter(category__in=recently_viewed_categories).exclude(id__in=recently_viewed_item_ids).distinct()[:4]
        print(1)
        print(fav_recommendations_queryset)

        personal_list = fav_recommendations_queryset | similar_items

        for item in recently_viewed_items:
            print(item.itemtitle)

        context = {
            'products': products,
            'cartItems': cartItems,
            'customer': customer_data ,
            'categories': categories ,
            'sellers': sellers,
            'similar_items': similar_items,
            'fav_recommendations_queryset': fav_recommendations_queryset,
            'personal_list':personal_list
        }

        return render(request, 'customer/personalgrocerylist.html', context)
    else:
        return redirect('logincustomer')
        