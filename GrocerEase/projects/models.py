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
 
