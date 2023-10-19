from django.urls import path
from . import views

app_name='cart'

    
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add_cart/<int:product_id>', views.add_cart, name='add_cart'), 
    path('delete_cart/<int:cart_id>', views.delete_cart, name='delete_cart'), 
  
]