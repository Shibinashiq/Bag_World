from django.urls import path
from . import views

app_name='admin_side'

    
urlpatterns = [
    
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    
    
    path('admin_user/', views.admin_user, name='admin_user'),
    path('user_block/<int:user_id>', views.user_block, name='user_block'),
    path('user_unblock/<int:user_id>', views.user_unblock, name='user_unblock'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('brand/',views.brand,name='brand'),
    path('add_brand/',views.add_brand,name='add_brand'),
    path('edit_brand/<int:brand_id>/', views.edit_brand, name='edit_brand'),
    path('brand_delete/<int:brand_id>/', views.brand_delete, name='brand_delete'),
   
    path('category', views.category, name='category'),
    path('add_category', views.add_category, name='add_category'),
    path('edit_category/<int:cat_id>/', views.edit_category, name='edit_category'),
    path('category_delete/<int:cat_id>/', views.category_delete, name='category_delete'),
   
    path('product',views.product,name='product'),
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/<int:product_id>',views.edit_product,name='edit_product'),
    path('product_delete/<int:product_id>',views.product_delete,name='product_delete'),
    path('product_undelete/<int:product_id>',views.product_undelete,name='product_undelete'),
    
    
    
     path('orders',views.orders,name='orders'),
     
    path('offer',views.offer,name='offer'),
    path('add_offer',views.add_offer,name='add_offer'),
    path('edit_offer/<int:offer_id>/',views.edit_offer,name='edit_offer'), 
    path('offer_delete/<int:offer_id>/', views.offer_delete, name='offer_delete'),
    path('offer_undelete/<int:offer_id>/', views.offer_undelete, name='offer_undelete'),

    
    
    path('coupon',views.coupon,name='coupon'),
    path('add_coupon',views.add_coupon,name='add_coupon'),
    path('edit_coupon/<int:coupon_id>/',views.edit_coupon,name='edit_coupon'), 
    path('coupon_delete/<int:coupon_id>/',views.coupon_delete,name='coupon_delete'),
    path('coupon_undelete/<int:coupon_id>/',views.coupon_undelete,name='coupon_undelete'),
    

]