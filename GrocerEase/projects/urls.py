from django.urls import path
from . import views

from .views.customer.registration.register import registercustomer
from .views.customer.verification.verifyotp import verifyotpcustomer
from .views.customer.login.login import logincustomer
from .views.customer.homepage.home import homecustomer
from .views.customer.profile.myprofile import customerprofile
from .views.customer.logout.logout import logoutcustomer
from .views.customer.cart.viewcart import cart
from .views.customer.itemdetails.viewdetails import itemdetails
from .views.customer.cart.updatecart import updatecart
from .views.customer.checkout.checkout import checkout
from .views.customer.resetpassword.sendresetotp import sendcustomerresetotp
from .views.customer.resetpassword.verifyresetotp import verifycustomerresetotp
from .views.customer.resetpassword.newpassword import changecustomerpassword
from .views.customer.search.searchitems import searchitems
from .views.customer.shopnavbar.viewshop import viewshop


from .views.seller.registration.register import registerseller
from .views.seller.verification.verifyotp import verifyotpseller
from .views.seller.login.login import loginseller
from .views.seller.logout.logout import logoutseller
from .views.seller.homepage.home import homeseller
from .views.seller.profile.myprofile import sellerprofile
from .views.seller.itemactions.uploaditem import uploaditem
from .views.seller.itemactions.updateitem import updateitem
from .views.seller.itemactions.deleteitem import deleteitem
from .views.seller.items.viewdetails import myitemdetails
from .views.seller.items.myitems import myitems
from .views.seller.resetpassword.sendotp import sendsellerresetotp
from .views.seller.resetpassword.verifyotp import verifysellerresetotp
from .views.seller.resetpassword.newpassword import changesellerpassword


# from .views import reset_password, verify_reset_otp, change_password
urlpatterns = [
    # path('', registercustomer, name="signupcustomer"), 
    # '' --> root domain
    path('signupcustomer/', registercustomer, name='signupcustomer'),

    path('logincustomer/', logincustomer, name='logincustomer'),

    path('logoutcustomer/', logoutcustomer, name='logoutcustomer'),

    path('verify_otpcustomer/', verifyotpcustomer, name='verify_otpcustomer'),

    path('homecustomer/<int:customer_id>/', homecustomer, name='homecustomer'),

    path('customerprofile/<int:customer_id>/', customerprofile, name='customerprofile'),

    path('signupseller/', registerseller, name='signupseller'),

    path('loginseller/', loginseller, name='loginseller'),

    path('logoutseller/', logoutseller, name='logoutseller'),

    path('verify_otpseller/', verifyotpseller, name='verify_otpseller'),

    path('homeseller/<int:seller_id>/', homeseller, name='homeseller'),

    path('sellerprofile/<int:seller_id>/', sellerprofile, name='sellerprofile'),

    path('uploaditem/<int:seller_id>/', uploaditem, name='uploaditem'),

    path('itemdetails/<str:pk>/', myitemdetails, name="singleitem"),

    path('updateitem/<str:pk>/', updateitem, name="updateitem"),

    path('deleteitem/<str:pk>/', deleteitem, name="deleteitem"),

    path('cart/<int:customer_id>/', cart, name="cart"),

    path('checkout/<int:customer_id>/', checkout, name="checkout"),

    path('updatecart/', updatecart, name="updatecart"),

    path('myitems/<int:seller_id>/', myitems, name="myselleritem"),

    
   # path('searchseller/<int:seller_id>/', views.searchseller, name="searchseller"),

    path('itemdetails/<str:pk>/', itemdetails, name="singleitemcustomer"),

    path('resetpassword/', sendcustomerresetotp, name='reset_password'),

    path('verifyresetotp/<str:email>/', verifycustomerresetotp, name='verify_reset_otp'),

    path('changeassword/<str:email>/', changecustomerpassword, name='change_password'),

    path('search/<int:customer_id>/', searchitems, name="search"),

    path('shop/<int:customer_id>/', viewshop, name="shop"),

    path('resetsellerpassword/', sendsellerresetotp, name='reset_seller_password'),
    path('verifyresetseller_otp/<str:email>/', verifysellerresetotp, name='verify_reset_seller_otp'),
    path('changesellerpassword/<str:email>/', changesellerpassword, name='change_seller_password'),
    



] 
