from django.urls import path
from . import views
from .views import reset_password, verify_reset_otp, change_password
urlpatterns = [
    path('', views.registercustomer, name="signupcustomer"), 
    # '' --> root domain
    
    path('signupcustomer/', views.registercustomer, name='signupcustomer'),

    path('logincustomer/', views.logincustomer, name='logincustomer'),

    path('logoutcustomer/', views.logoutcustomer, name='logoutcustomer'),

    path('verify_otpcustomer/', views.verifyotpcustomer, name='verify_otpcustomer'),

    path('homecustomer/<int:customer_id>/', views.homecustomer, name='homecustomer'),

    path('customerprofile/<int:customer_id>/', views.customerprofile, name='customerprofile'),

    path('signupseller/', views.registerseller, name='signupseller'),

    path('loginseller/', views.loginseller, name='loginseller'),

    path('logoutseller/', views.logoutseller, name='logoutseller'),

    path('verify_otpseller/', views.verifyotpseller, name='verify_otpseller'),

    path('homeseller/<int:seller_id>/', views.homeseller, name='homeseller'),

    path('sellerprofile/<int:seller_id>/', views.sellerprofile, name='sellerprofile'),

    path('uploaditem/<int:seller_id>/', views.uploadItem, name='uploaditem'),

    path('singleitem/<str:pk>/', views.singleitem, name="singleitem"),

    path('updateitem/<str:pk>/', views.updateItemSeller, name="updateitem"),

    path('deleteitem/<str:pk>/', views.deleteItem, name="deleteitem"),

    path('cart/<int:customer_id>/', views.cart, name="cart"),

    path('checkout/<int:customer_id>/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),

    path('myitem/<int:seller_id>/', views.myItem, name="myselleritem"),

    path('singleitemcustomer/<str:pk>/', views.singleitemcustomer, name="singleitemcustomer"),
    path('reset_password/', reset_password, name='reset_password'),
    path('verify_reset_otp/<str:email>/', verify_reset_otp, name='verify_reset_otp'),
    path('change_password/<str:email>/', change_password, name='change_password'),


] 
