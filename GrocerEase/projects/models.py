from django.db import models
import uuid

class Customer(models.Model):
    customername = models.CharField(max_length=150, unique=True)
    customeremail = models.EmailField(unique=True)
    customerpassword = models.CharField(max_length=128)
    otp = models.CharField(max_length=6, blank=True, null=True)  
    is_verified = models.BooleanField(default=False) 

    def __str__(self):
        return self.customername

class Seller(models.Model):
    storename = models.CharField(max_length=150, unique=True)
    selleremail = models.EmailField(unique=True)
    sellerpassword = models.CharField(max_length=128)
    otp = models.CharField(max_length=6, blank=True, null=True)  
    is_verified = models.BooleanField(default=False) 

    def __str__(self):
        return self.storename


class Item(models.Model):
    itemtitle = models.CharField(max_length=200) # null by default is set as false. so it is must
    itemprice = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    itemquantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    itemdescription = models.TextField(null=True, blank=True) # null is for database to know even if there's no description we can still create a record/row. blank is similar as that for django to know about it
    itemfeaturedimage = models.ImageField(null=True, blank=True, default="")
    CATEGORY_TYPE = (
        ('veg', 'veg'),
        ('nonveg', 'nonveg'),
    )
    uploadedon = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) #uuid4 is for encoding

    def __str__(self):
        return self.itemtitle


