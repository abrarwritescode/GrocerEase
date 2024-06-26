from projects.imports import *
from projects.recommendation_utils import generate_item_features, calculate_similarity, get_recommendations

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def itemsrecommendation(request, customer_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('home')
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id'] 
        customer = Customer.objects.get(pk=customer_id)

        all_items = list(Item.objects.all())
        customer_favorites = list(Favorite.objects.filter(customer=customer))

        customer_item_features = generate_item_features(all_items)
        customer_similarity_matrix = calculate_similarity(customer_item_features)

        recommendations_list = []

        for favorite_item in customer_favorites:
            # index of the favorite item within the list of items
            item_index = all_items.index(favorite_item.item)

            recommendations = get_recommendations(item_index, all_items, customer_similarity_matrix)

            recommendations_list.extend(recommendations)

            request.session['recommendations_list'] = recommendations_list

        context = {
            'customer': customer,
            'recommendations_list': recommendations_list,
        }

        return render(request, 'customer/itemsrecommendation.html', context)
    else:
        
        return redirect('logincustomer')
