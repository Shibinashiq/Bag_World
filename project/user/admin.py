from django.contrib import admin
from .models import Order, Profile,Wallet,Transaction

admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(Wallet)
admin.site.register(Transaction)
