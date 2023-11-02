from decimal import Decimal
from django.db import models
from admin_side.models import Product  # Import the Products model from your 'items' app
from django.contrib.auth.models import User

 

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateField( auto_now_add=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username   
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(  auto_now_add= True)
    
class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    discount = models.PositiveSmallIntegerField()
    
