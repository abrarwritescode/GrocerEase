from projects.imports import *
from django.db.models import Avg

from django.shortcuts import render, redirect
from projects.forms import ReviewForm
from django.views.decorators.cache import cache_control

from django.shortcuts import get_object_or_404

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def submit_review(request, item_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(pk=request.session['customer_id'])
            item = get_object_or_404(Item, pk=item_id)

            
            orders = Order.objects.filter(customer=customer)
            customercanreview = 0

            for order in orders:
                if order.status == 'Delivered':
                    ordered_item = OrderItem.objects.filter(order=order, product=item).first()
                    if ordered_item:
                        customercanreview = 1
                        break

            
            if not customercanreview:
                return redirect('singleitemcustomer', pk=item_id, customer_id=request.session['customer_id'])

            existing_review = Review.objects.filter(customer=customer, item=item)
            if existing_review.exists():
                return redirect('singleitemcustomer', pk=item_id, customer_id=request.session['customer_id'])

            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            Review.objects.create(item=item, customer=customer, rating=rating, comment=comment)

    return redirect('singleitemcustomer', pk=item_id, customer_id=request.session['customer_id'])
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def item_details_with_reviews(request, pk, customer_id):
    if 'sessionid' not in request.COOKIES:
        return redirect('home')   
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
    
    reviews = Review.objects.filter(item=itemObj)

    customer_has_reviewed = Review.objects.filter(item=itemObj, customer=customer).exists()
    
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    average_rating = round(average_rating, 2)

    rating1=0
    rating2=0
    rating3=0
    rating4=0
    rating5=0
    for review in reviews:
        if (review.rating==1):
            rating1+=1
        if (review.rating==2):
            rating2+=1
        if (review.rating==3):
            rating3+=1
        if (review.rating==4):
            rating4+=1
        if (review.rating==5):
            rating5+=1

    recently_viewed = request.session.get('recently_viewed', [])
    if pk not in recently_viewed:
        recently_viewed.insert(0, pk)
        request.session['recently_viewed'] = recently_viewed[:5] 

    complementary_items = itemObj.get_complementary_items()
    orders = Order.objects.filter(customer=customer)
    customercanreview = any(
        order.status == 'Delivered' and OrderItem.objects.filter(order=order, product=itemObj).exists()
        for order in orders
    )
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            Review.objects.create(item=itemObj, customer=customer, rating=rating, comment=comment)
            
            return redirect('item_details_with_reviews', pk=pk, customer_id=customer_id)
    else:
        form = ReviewForm()

    return render(request, 'customer/singleitemcustomer.html', {
        'item': itemObj,
        'categorys': categorys,
        'products': products,
        'cartItems': cartItems,
        'customer': customer,
        'categories': categories,
        'reviews': reviews,
        'review_form': form,
        'average_rating': average_rating,
        'customer_has_reviewed': customer_has_reviewed, 
        'complementary_items': complementary_items,
        'rating1':rating1,
        'rating2':rating2,
        'rating3':rating3,
        'rating4':rating4,
        'rating5':rating5,
        'customercanreview': customercanreview,
        
    })