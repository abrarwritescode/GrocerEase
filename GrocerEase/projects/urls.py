from django.urls import path

from .views.customer.imports.customerviewsimport import *

from .views.seller.imports.sellerviewsimport import *


urlpatterns = [
    path('signupcustomer/', registercustomer, name='signupcustomer'),
    path('verify_otpcustomer/', verifyotpcustomer, name='verify_otpcustomer'),
    path('logincustomer/', logincustomer, name='logincustomer'),
    path('homecustomer/<int:customer_id>/', homecustomer, name='homecustomer'),
    path('customerprofile/<int:customer_id>/', customerprofile, name='customerprofile'),
    path('logoutcustomer/', logoutcustomer, name='logoutcustomer'),
    path('cart/<int:customer_id>/', cart, name="cart"),
    path('itemdetails/<str:pk>/<int:customer_id>/', itemdetails, name="singleitemcustomer"),
    path('updatecart/', updatecart, name="updatecart"),
    path('checkout/<int:customer_id>/', checkout, name="checkout"),
    path('resetpassword/', sendcustomerresetotp, name='reset_password'),
    path('verifyresetotp/<str:email>/', verifycustomerresetotp, name='verify_reset_otp'),
    path('changeassword/<str:email>/', changecustomerpassword, name='change_password'),
    path('search/<int:customer_id>/', searchitems, name="search"),
    path('shop/<int:customer_id>/', viewshop, name="shop"),
    path('filterbycategory/<str:category_name>/<int:customer_id>/', filteritemsbycategory, name='filteritemsbycategory'),
    path('filterbyprice/', filteritemsbyprice, name='filteritemsbyprice'),

    path('selleritems/<int:seller_id>/', selleritems, name='selleritems'),
    
    path('signupseller/', registerseller, name='signupseller'),
    path('verify_otpseller/', verifyotpseller, name='verify_otpseller'),
    path('loginseller/', loginseller, name='loginseller'),
    path('logoutseller/', logoutseller, name='logoutseller'),
    path('homeseller/<int:seller_id>/', homeseller, name='homeseller'),
    path('sellerprofile/<int:seller_id>/', sellerprofile, name='sellerprofile'),
    path('myitems/<int:seller_id>/', myitems, name="myselleritem"),
    path('myitemdetails/<str:pk>/', myitemdetails, name="singleitem"),
    path('uploaditem/<int:seller_id>/', uploaditem, name='uploaditem'),
    path('updateitem/<str:pk>/', updateitem, name="updateitem"),
    path('deleteitem/<str:pk>/', deleteitem, name="deleteitem"),
    path('searchseller/<int:seller_id>/', sellersearch, name='searchseller'),
    path('resetsellerpassword/', sendsellerresetotp, name='reset_seller_password'),
    path('verifyresetseller_otp/<str:email>/', verifysellerresetotp, name='verify_reset_seller_otp'),
    path('changesellerpassword/<str:email>/', changesellerpassword, name='change_seller_password'),
] 
