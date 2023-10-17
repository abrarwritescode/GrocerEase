from django.contrib import admin

# Register your models here.

from .models import Customer, Seller, Item, Order, OrderItem, Category

admin.site.register(Customer)

admin.site.register(Seller)

admin.site.register(Item)

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(Category)




