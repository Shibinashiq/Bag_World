from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_wishlist/<int:product_id>/', views.add_wishlist, name='add_wishlist'),
    path('remove_wishlist/<int:product_id>/', views.remove_wishlist, name='remove_wishlist'),

    
    
    path('add_cart', views.add_cart, name='add_cart'),
    
    path('wishlist_to_cart/<int:wishlist_id>/', views.wishlist_to_cart, name='wishlist_to_cart'),
    
    path('update_cart',views.update_cart , name='update_cart'),
    
    
    path('multiple_address',views.multiple_address, name='multiple_address'),
    
    path('generate_coupon/', views.generate_coupon, name='generate_coupon'),
    
    
    

  
    # path('decrease_cart/<int:product_id>/', views.decrease_cart, name='decrease_cart'),

  
    # path('delete_cart_item/<int:product_id>/', views.delete_cart_item, name='delete_cart_item'),
    
     path('checkout/', views.checkout, name='checkout'),
]