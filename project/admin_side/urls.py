from django.urls import path
from . import views

app_name='admin_side'

    
urlpatterns = [
    
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_user/', views.admin_user, name='admin_user'),
    path('user_block/<int:user_id>', views.user_block, name='user_block'),
    path('user_unblock/<int:user_id>', views.user_unblock, name='user_unblock'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('brand/',views.brand,name='brand'),
    path('add_brand/',views.add_brand,name='add_brand'),
    path('edit_brand/<int:brand_id>/', views.edit_brand, name='edit_brand'),
    path('brand_delete/<int:brand_id>/', views.brand_delete, name='brand_delete'),
    path('brand_undelete/<int:brand_id>/', views.brand_undelete, name='brand_undelete'),
    path('category', views.category, name='category'),
    path('add_category', views.add_category, name='add_category'),
    path('edit_category/<int:cat_id>/', views.edit_category, name='edit_category'),
    path('category_delete/<int:cat_id>/', views.category_delete, name='category_delete'),
    path('category_undelete/<int:cat_id>/', views.category_undelete, name='category_undelete'),
    path('product',views.product,name='product'),
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/<int:product_id>',views.edit_product,name='edit_product'),
    path('product_delete/<int:product_id>',views.product_delete,name='product_delete'),
    path('product_undelete/<int:product_id>',views.product_undelete,name='product_undelete'),
     

]