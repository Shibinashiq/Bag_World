from django.db import models
from datetime import datetime
from django.utils import timezone

class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    brand_image = models.ImageField(upload_to='brands_image/')  # You'll need to configure MEDIA_ROOT and MEDIA_URL
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.brand_name
 
class Category(models.Model):
    cat_image = models.ImageField(upload_to='cat_photos/')
    category_name = models.CharField(max_length=25)
    is_deleted = models.BooleanField(default=False)

    description = models.TextField()  # Add a field for description
    

    def __str__(self):
        return self.category_name  # Define a string representation for the model
    

class Offer(models.Model):
    offer_name = models.CharField(max_length=50, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField(default=datetime.now)  # Use datetime from the imported module
    end_date = models.DateField(default=datetime.now)  # Use datetime from the imported module
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
            return self.offer_name
        
class Product(models.Model):   
    product_image = models.ImageField(upload_to='product_image/' , null=True)
    product_name = models.CharField(max_length=255 , null=True)  # Changed to CharField for product name
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Changed to DecimalField for product price
    product_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)  # Changed to CharField for product brand
    product_offer = models.ForeignKey(Offer,on_delete=models.CASCADE, null=True,blank=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField(null=True)  # Changed to PositiveIntegerField for quantity
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.product_name
    
class ProductImage(models.Model):
    image=models.ImageField(upload_to='product_image/',null=True) 
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50)
    discount = models.PositiveIntegerField()
    min_price = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_name




