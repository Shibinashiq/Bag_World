from datetime import timedelta
from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from admin_side.models import Product


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    streetaddress = models.CharField(max_length=255)
    town = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    ordernote = models.TextField()
    company_name = models.CharField(max_length=100)  # Add company name field
    country = models.CharField(max_length=100)  # Add country field

    def __str__(self):
        return f"{self.firstname} {self.lastname}'profile"


class Order(models.Model):
    product=models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)
    total_price = models.IntegerField(null=True) 
    payment_mode = models.CharField( max_length=50,default=True)
    payment_id = models.CharField( max_length=50,blank=True,null=True,default=True)
    messages = models.TextField(blank=True,null=True,default=True)
    tracking_no =models.CharField( max_length=50,default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    update_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    is_cancelled = models.BooleanField(default=False)
    ordertatus= {
        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Return', 'Return')       
    }
    od_status = models.CharField( max_length=150 , default='pending',choices=ordertatus , null=True)
    @property
    def expected_delivery(self):
        return self.created_at + timedelta(days=7)
    def __str__(self):
        return f"Order {self.id} for {self.user.first_name}"
