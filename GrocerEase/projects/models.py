from django.db import models
import uuid

class Customer(models.Model):
    customername = models.CharField(max_length=150, unique=True)
    customeremail = models.EmailField(unique=True)
    customerpassword = models.CharField(max_length=128)
    otp = models.CharField(max_length=6, blank=True, null=True)  
    is_verified = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.id} - {self.customername}"

class Seller(models.Model):
    storename = models.CharField(max_length=150, unique=True)
    selleremail = models.EmailField(unique=True)
    sellerpassword = models.CharField(max_length=128)
    otp = models.CharField(max_length=6, blank=True, null=True)  
    is_verified = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.id} - {self.storename}"


class Item(models.Model):
    seller =  models.ForeignKey(Seller, on_delete=models.CASCADE, default=1)
    itemtitle = models.CharField(max_length=200) # null by default is set as false. so it is must
    itemprice = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    itemquantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    itemdescription = models.TextField(null=True, blank=True) # null is for database to know even if there's no description we can still create a record/row. blank is similar as that for django to know about it
    itemfeaturedimage = models.ImageField(null=True, blank=True, default="default_img.png")
    uploadedon = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) #uuid4 is for encoding

    def __str__(self):
        return self.itemtitle

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return f"{self.id} - {self.customer}"
		
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
    product = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OrderItem {self.order} - {self.product.itemtitle}"
      
    @property
    def get_total(self):
        total = self.product.itemprice * self.quantity
        return total
