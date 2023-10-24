from django.db import models

# Create your models here.
from django.contrib.auth.models import User


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
        return f"{self.firstname} {self.lastname}'s Order"
