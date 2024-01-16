from projects.imports import *
from collections import defaultdict
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

        most_bought_items = customer.get_most_bought_items(num_items=5)
        print('a')
        print('b')
        print(most_bought_items)

        most_bought_items_by_count = customer.get_most_bought_items_by_count(num_items=5)
        print('c')
        print(2)
        print(most_bought_items_by_count)
        combined_list = most_bought_items + most_bought_items_by_count
        print(combined_list)



        combined_dict = defaultdict(lambda: {'item': None, 'total_quantity': 0, 'count': 0})


        for item in most_bought_items:
            item_key = item.get('item')
            combined_dict[item_key]['item'] = item_key
            combined_dict[item_key]['total_quantity'] += item.get('total_quantity', 0)

        for item in most_bought_items_by_count:
            item_key = item.get('item')
            combined_dict[item_key]['item'] = item_key
            combined_dict[item_key]['count'] += item.get('count', 0)

   
        combined_list = list(combined_dict.values())

        print(combined_list)


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

        # combined_list_ids = [item.id for Item in combined_list]
        # combined_list_queryset = Item.objects.filter(id__in=combined_list_ids)
    #     for item_data in combined_list:
    #         item_object = item_data['item']
    
    # # Assuming 'id' is the attribute in the 'Item' class representing the ID
    #         item_id = getattr(item_object, 'id', None)
    
    #         print(f"Item ID: {item_id}")


    #     print(555)
        # print(combined_list_queryset)

        item_ids_list = [getattr(item_data['item'], 'id', None) for item_data in combined_list]

# Filter items based on the IDs
        combined_queryset = Item.objects.filter(id__in=item_ids_list)


        recently_viewed_item_ids = request.session.get('recently_viewed', [])
        recently_viewed_items = Item.objects.filter(id__in=recently_viewed_item_ids)

        recently_viewed_categories = Item.objects.filter(id__in=recently_viewed_item_ids).values_list('category', flat=True)


        similar_items = Item.objects.filter(category__in=recently_viewed_categories).exclude(id__in=recently_viewed_item_ids).distinct()[:4]
        print(1)
        print(fav_recommendations_queryset)

        personal_list = fav_recommendations_queryset | similar_items | combined_queryset

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
            'personal_list':personal_list,
            'combined_list':combined_list,
            # 'combined_queryset':combined_queryset
        }

        return render(request, 'customer/personalgrocerylist.html', context)
    else:
        return redirect('logincustomer')
        