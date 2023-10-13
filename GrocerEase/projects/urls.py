from django.urls import path
from . import views

urlpatterns = [
    path('', views.registercustomer, name="signupcustomer"), 
    # '' --> root domain
    
    path('signupcustomer/', views.registercustomer, name='signupcustomer'),

    path('logincustomer/', views.logincustomer, name='logincustomer'),

    path('logoutcustomer/', views.logoutcustomer, name='logoutcustomer'),

    path('verify_otpcustomer/', views.verifyotpcustomer, name='verify_otpcustomer'),

    path('homecustomer/<int:customer_id>/', views.homecustomer, name='homecustomer'),

    path('signupseller/', views.registerseller, name='signupseller'),

    path('loginseller/', views.loginseller, name='loginseller'),

    path('logoutseller/', views.logoutseller, name='logoutseller'),

    path('verify_otpseller/', views.verifyotpseller, name='verify_otpseller'),

    path('homeseller/<int:seller_id>/', views.homeseller, name='homeseller'),

    path('uploaditem/', views.uploadItem, name='uploaditem'),

    path('singleitem/<str:pk>/', views.singleitem, name="singleitem"),

    path('updateitem/<str:pk>', views.updateItem, name="updateitem"),

    path('deleteitem/<str:pk>', views.deleteItem, name="deleteitem"),

    path('cart/<int:customer_id>/', views.cart, name="cart"),

    path('checkout/<int:customer_id>/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),


] 
