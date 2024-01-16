from django.urls import path

from .views.customer.imports.customerviewsimport import * 

from .views.seller.imports.sellerviewsimport import *

from .views.guestuser.imports.guestuserimports import *

from .views.errors import custom_error_page



urlpatterns = [
    path('', non_logged_in_home, name='home'),
    path('guestselleritems/<int:seller_id>/', guestselleritems, name='guestselleritems'),

    path('signupcustomer/', registercustomer, name='signupcustomer'),
    path('verify_otpcustomer/', verifyotpcustomer, name='verify_otpcustomer'),
    path('logincustomer/', logincustomer, name='logincustomer'),
    path('homecustomer/<int:customer_id>/', homecustomer, name='homecustomer'),
    path('customerprofile/<int:customer_id>/', customerprofile, name='customerprofile'),
    path('logoutcustomer/', logoutcustomer, name='logoutcustomer'),
    path('cart/<int:customer_id>/', cart, name="cart"),
    path('itemdetails/<str:pk>/<int:customer_id>/', item_details_with_reviews, name="singleitemcustomer"),
    path('updatecart/', updatecart, name="updatecart"),
    path('deletecart/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('checkout/<int:customer_id>/', checkout, name="checkout"),
    path('resetpassword/', sendcustomerresetotp, name='reset_password'),
    path('verifyresetotp/<str:email>/', verifycustomerresetotp, name='verify_reset_otp'),
    path('changeassword/<str:email>/', changecustomerpassword, name='change_password'),
    path('search/<int:customer_id>/', searchitems, name="search"),
    path('shop/<int:customer_id>/', viewshop, name="shop"),
    path('filterbycategory/<str:category_name>/<int:customer_id>/', filteritemsbycategory, name='filteritemsbycategory'),
    path('filterbyprice/<int:customer_id>/', filteritemsbyprice, name='filteritemsbyprice'),
    path('myfavorites/<int:customer_id>/', viewfavorites, name='myfavorites'),
    path('getfavoritescount/<int:customer_id>/', getfavoritescount, name='getfavoritescount'), 
    path('togglefavorite/<str:pk>/<int:customer_id>/', togglefavorite, name='togglefavorite'),
    path('check_voucher/', check_voucher, name='check_voucher'),
    path('save_updated_price/', SaveUpdatedPriceView.as_view(), name='save_updated_price'),
    path('itemsrecommendation/<int:customer_id>/', itemsrecommendation, name='itemsrecommendation'),
    path('personalgrocerylist/<int:customer_id>/', personalgrocerylist, name='personalgrocerylist'),

   
    path('selleritems/<int:seller_id>/<int:customer_id>/', selleritems, name='selleritems'),
    
    path('signupseller/', registerseller, name='signupseller'),
    path('verify_otpseller/', verifyotpseller, name='verify_otpseller'),
    path('loginseller/', loginseller, name='loginseller'),
    path('logoutseller/', logoutseller, name='logoutseller'),
    path('homeseller/<int:seller_id>/', homeseller, name='homeseller'),
    path('sellerprofile/<int:seller_id>/', sellerprofile, name='sellerprofile'),
    path('myitems/<int:seller_id>/', myitems, name="myselleritem"),
    path('myitemdetails/<str:pk>/<int:seller_id>/', myitemdetails, name="singleitem"),
    path('uploaditem/<int:seller_id>/', uploaditem, name='uploaditem'),
    path('updateitem/<str:pk>/', updateitem, name="updateitem"),
    path('deleteitem/<str:pk>/', deleteitem, name="deleteitem"),
    path('searchseller/<int:seller_id>/', sellersearch, name='searchseller'),
    path('resetsellerpassword/', sendsellerresetotp, name='reset_seller_password'),
    path('verifyresetseller_otp/<str:email>/', verifysellerresetotp, name='verify_reset_seller_otp'),
    path('changesellerpassword/<str:email>/', changesellerpassword, name='change_seller_password'),
    path('sellernotifications/<int:seller_id>/', sellernotifs, name='notifications'),
    path('getnotificationcount/<int:seller_id>/', getnotificationcount, name='getnotificationcount'),
    path('marknotificationsasread/<int:seller_id>/', marknotificationsasread, name='marknotificationsasread'),
    path('customer/<int:customer_id>/change-image/',change_customer_image, name='change_customer_image'),
    path('clearsinglenotif/<int:notification_id>/<int:seller_id>/', clearsinglenotif, name='clearsinglenotif'),
    path('orders/<int:seller_id>/', vieworders, name='vieworders'),
    path('submit_review/<uuid:item_id>/',submit_review, name='submit_review'),
    
    path('<path:not_found>/', custom_error_page, name='404'),
] 




