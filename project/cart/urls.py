from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart, name='cart'),

    
    path('add_cart', views.add_cart, name='add_cart'),
    
    
    path('update_cart',views.update_cart , name='update_cart'),

  
    # path('decrease_cart/<int:product_id>/', views.decrease_cart, name='decrease_cart'),

  
    # path('delete_cart_item/<int:product_id>/', views.delete_cart_item, name='delete_cart_item'),
    
     path('checkout/', views.checkout, name='checkout'),
]