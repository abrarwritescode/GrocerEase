from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name="signup"), 
    # '' --> root domain
    
    path('signup/', views.register, name='signup'),

    path('login/', views.login, name='login'),

    path('logout/', views.logout, name='logout'),

    path('verify_otp/', views.verify_otp, name='verify_otp'),
]
