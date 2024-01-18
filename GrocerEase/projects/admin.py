from django.contrib import admin

# Register your models here.

from .models import Customer, Seller, Item, Order, OrderItem, Category, Notification, Favorite, VoucherCode ,Review, Refund

admin.site.register(Customer)

admin.site.register(Seller)

admin.site.register(Item)

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(Category)

admin.site.register(Notification)

admin.site.register(Favorite)

admin.site.register(VoucherCode)

admin.site.register(Review)


admin.site.register(Refund)