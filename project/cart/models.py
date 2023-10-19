from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User

from admin_side.models import Product 

# Create your models here. 
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False , null=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateField( auto_now_add=True)

    def str(self) -> str:
        return self.user.username