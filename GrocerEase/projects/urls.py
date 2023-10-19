from django.urls import path
from . import views

from .views.customer.registration.register import registercustomer
from .views.customer.verification.verifyotp import verifyotpcustomer
from .views.customer.login.login import logincustomer
from .views.customer.homepage.home import homecustomer
from .views.customer.profile.profile import customerprofile
from .views.customer.logout.logout import logoutcustomer
from .views.customer.cart.viewcart import cart
from .views.customer.itemdetails.viewdetails import itemdetails
from .views.customer.cart.updatecart import updatecart
from .views.customer.checkout.checkout import checkout
from .views.customer.resetpassword.sendresetotp import sendresetotp
from .views.customer.resetpassword.verifyresetotp import verifyresetotp
from .views.customer.resetpassword.newpassword import changepassword
from .views.customer.search.searchitems import searchitems
from .views.customer.shopnavbar.viewshop import viewshop



 


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

    # path('signupseller/', views.registerseller, name='signupseller'),

    # path('loginseller/', views.loginseller, name='loginseller'),

    # path('logoutseller/', logoutseller, name='logoutseller'),

    # path('verify_otpseller/', views.verifyotpseller, name='verify_otpseller'),

    # path('homeseller/<int:seller_id>/', views.homeseller, name='homeseller'),

    # path('sellerprofile/<int:seller_id>/', views.sellerprofile, name='sellerprofile'),

    # path('uploaditem/<int:seller_id>/', views.uploadItem, name='uploaditem'),

    # path('singleitem/<str:pk>/', views.singleitem, name="singleitem"),

    # path('updateitem/<str:pk>/', views.updateItemSeller, name="updateitem"),

    # path('deleteitem/<str:pk>/', views.deleteItem, name="deleteitem"),

    path('cart/<int:customer_id>/', cart, name="cart"),

    path('checkout/<int:customer_id>/', checkout, name="checkout"),

    path('updatecart/', updatecart, name="updatecart"),

    # path('myitem/<int:seller_id>/', views.myItem, name="myselleritem"),

    path('itemdetails/<str:pk>/', itemdetails, name="singleitemcustomer"),

    path('resetpassword/', sendresetotp, name='reset_password'),

    path('verifyresetotp/<str:email>/', verifyresetotp, name='verify_reset_otp'),

    path('changeassword/<str:email>/', changepassword, name='change_password'),

    path('search/<int:customer_id>/', searchitems, name="search"),

    path('shop/<int:customer_id>/', viewshop, name="shop"),



] 
