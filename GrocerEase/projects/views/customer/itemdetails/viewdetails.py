from projects.imports import *
from django.db.models import Avg

from django.shortcuts import render, redirect
from projects.forms import ReviewForm

def submit_review(request, item_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(pk=request.session['customer_id'])
            item = Item.objects.get(pk=item_id)
          
            
            existing_review = Review.objects.filter(customer=customer, item=item)
            if existing_review.exists():

                return redirect('singleitemcustomer', pk=item_id, customer_id=request.session['customer_id'])

            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            Review.objects.create(item=item, customer=customer, rating=rating, comment=comment)
    return redirect('singleitemcustomer', pk=item_id,  customer_id=request.session['customer_id'])

def item_details_with_reviews(request, pk, customer_id):
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

    recently_viewed = request.session.get('recently_viewed', [])
    if pk not in recently_viewed:
        recently_viewed.insert(0, pk)
        request.session['recently_viewed'] = recently_viewed[:5] 

    complementary_items = itemObj.get_recommendations(customer)
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
        
    })
