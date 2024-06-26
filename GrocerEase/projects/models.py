from itertools import count
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
import uuid

class NonDeleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)

class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False)
    everything = models.Manager()
    objects = NonDeleted()

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True

class Customer(models.Model):
    customername = models.CharField(max_length=150)
    customeremail = models.EmailField(unique=True) 
    customerpassword = models.CharField(max_length=128)
    otp = models.CharField(max_length=6, blank=True, null=True)  
    is_verified = models.BooleanField(default=False) 
    customerimage = models.ImageField(null=True, blank=True, default="user-default.png")

    def get_most_bought_items(self, num_items=2):
        
        customer_orders = Order.objects.filter(customer=self, is_cart=False)

        
        order_items = OrderItem.objects.filter(order__in=customer_orders).select_related('product')

        item_quantities = {}

        for order_item in order_items:
            if order_item.product.id not in item_quantities:
                item_quantities[order_item.product.id] = {'item': order_item.product, 'total_quantity': 0}

            item_quantities[order_item.product.id]['total_quantity'] += order_item.quantity

    
        sorted_items = sorted(item_quantities.values(), key=lambda x: x['total_quantity'], reverse=True)

        most_bought_items = sorted_items[:num_items]

        return most_bought_items
    
    def get_most_bought_items_by_count(self, num_items=2):
        customer_orders = Order.objects.filter(customer=self, is_cart=False)

        order_items = OrderItem.objects.filter(order__in=customer_orders).select_related('product')

        item_counts = {}

      
        for order_item in order_items:
            item_id = order_item.product.id
            if item_id not in item_counts:
                item_counts[item_id] = {'item': order_item.product, 'count': 0}

            item_counts[item_id]['count'] += 1  

        sorted_items = sorted(item_counts.values(), key=lambda x: x['count'], reverse=True)

        most_bought_items_by_count = sorted_items[:num_items]

        return most_bought_items_by_count
    
    def __str__(self):
        return f"{self.id} - {self.customername}"

class Seller(models.Model):
    storename = models.CharField(max_length=150)
    selleremail = models.EmailField(unique=True)
    sellerpassword = models.CharField(max_length=128)
    otp = models.CharField(max_length=6, blank=True, null=True)  
    is_verified = models.BooleanField(default=False) 
    sellerimage = models.ImageField(null=True, blank=True, default="user-default.png")

    def __str__(self):
        return f"{self.storename}"


class Item(SoftDelete):
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)
    itemtitle = models.CharField(max_length=200) # null by default is set as false. so it is must
    itemprice = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    category = models.ManyToManyField('Category', blank=True) # Category model is below so used '', otherwise don't need
    itemquantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    itemdescription = models.TextField(null=True, blank=True) # null is for database to know even if there's no description we can still create a record/row. blank is similar as that for django to know about it
    itemfeaturedimage = models.ImageField(null=True, blank=True, default="default_img.png")
    uploadedon = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) #uuid4 is for encoding
    favorite_count = models.IntegerField(default=0)

    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now().date()
        
        if self.end_date and self.end_date < timezone.now().date():
            self.discount_percentage = 0

        super().save(*args, **kwargs)
    
        
    def get_recommendations(self, customer):
        orders_with_current_item = OrderItem.objects.filter(
            product=self, 
            
        ).values_list('order', flat=True)

        recommended_items = Item.objects.filter(
            orderitem__order__in=orders_with_current_item
        ).exclude(id=self.id).distinct()

        customer_purchased_items = Item.objects.filter(
            orderitem__order__customer=customer, 
             orderitem__order__status='Processing'
         )
        recommended_items = recommended_items.exclude(id__in=customer_purchased_items)

        return recommended_items
    
    def get_complementary_items(self):

        selected_item = self  

        all_items = Item.objects.exclude(id=selected_item.id)

        complementary_items_dict = {}

        for accessory in all_items.filter(category__in=selected_item.category.all()):
            for category in accessory.category.all():
                if category not in complementary_items_dict:
                    complementary_items_dict[category] = set()

                if accessory.id != selected_item.id:
                    complementary_items_dict[category].add(accessory)

        complementary_items_dict = {category: list(items)[:4] for category, items in complementary_items_dict.items()}

        return complementary_items_dict
    
    def frequently_bought_products(self, customer):
       
        orders_with_current_item = OrderItem.objects.filter(
            product=self,
            confirmed=True,
        ).values_list('order', flat=True)

        frequently_bought_items = Item.objects.filter(
            orderitem__order__in=orders_with_current_item,
            orderitem__order__status='Delivered', 
        ).exclude(id=self.id).annotate(frequency=count('id')).order_by('-frequency')[:5]

        return frequently_bought_items

    
    def __str__(self):
        return self.itemtitle


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_cart = models.BooleanField(default=True)  # To indicate whether it's a cart or a confirmed order

    shipping_name = models.CharField(max_length=255, null=True, blank=True)
    shipping_email = models.EmailField(null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    shipping_phone = models.CharField(max_length=20, null=True, blank=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')


    def __str__(self):
        return f"{self.id} - {self.customer}"
        
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems]) if orderitems else 0
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems]) if orderitems else 0
        return total
    
    @property
    def move_items_from_cart(self):
        cart_items = OrderItem.objects.filter(order=self, confirmed=False)
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=self,
                product=cart_item.product,
                quantity=cart_item.quantity,
                confirmed=True 
            )
        
        cart_items.delete()



class VoucherCode(models.Model):
    vouchercode = models.CharField(max_length=200, unique=True)
    voucher_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=True)
    voucher_count = models.PositiveIntegerField(default=1)  

    def __str__(self):
        return self.vouchercode


class OrderItem(models.Model):
    product = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)  # To indicate whether it's a cart item or a confirmed order item
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refunding In Progress', 'Refunding In Progress'),
        ('Refunded', 'Refunded'),
    ]

    status = models.CharField(max_length=29, choices=STATUS_CHOICES, default='Pending')


    
    def __str__(self):
        return f"OrderItem {self.order}"

    @property
    def get_total(self):
        total = self.product.itemprice * self.quantity
        return total


class Category(models.Model):
    categoryname = models.CharField(max_length=200)
    categoryimage = models.ImageField(null=True, blank=True, default="default_img.png")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) #uuid4 is for encoding

    def __str__(self):
        return self.categoryname
    
class Notification(SoftDelete):
    sender = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    recipient = models.ForeignKey(Seller, on_delete=models.CASCADE)
   
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False) 


    def __str__(self):
        return f"Notification {self.id}"

class Favorite(SoftDelete):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Favorite {self.id}"
    

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'item')

    def __str__(self):
        return f"Review by {self.customer} for {self.item}"
    

class Refund(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Assuming you have a Customer model
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund #{self.id} - {self.customer}"