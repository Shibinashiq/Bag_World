from user import views
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
app_name='user'

urlpatterns = [
    path('',views.home,name='home'),
    path('user_login',views.user_login, name='user_login'),
    path('user_logout',views.user_logout, name='user_logout'),
    path('user_signup',views.user_signup, name='user_signup'),
    path('otp',views.otp_page,name='otp'),
    
    path('shop',views.shop,name='shop'),
    path('product_view/<int:product_id>/',views.product_view, name='product_view'),
    
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit_profile/<int:address_id>/', views.edit_profile, name='edit_profile'),
    
    
    
    path('place_order/', views.place_order, name='place_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('return_order/<int:order_id>/', views.return_order, name='return_order'),
    
    
    
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
    
    # path('wallet_item/', views.wallet_item, name='wallet_item'),

    # path('user_address',views.user_address, name='user_address'),
    # path('edit_address/<int:user_id>/',views.edit_address, name='edit_address'),
    
    
    
    # path('contact',views.contact,name='contact'),
    path('index',views.index,name='index'),
    # path('about_us',views.about_us,name='about_us.html'),
    # path('contact_page',views.contact_page,name='contact_page.html'),
   
    
    
    # path('admin_dashboard.html', views.admin_dashboard, name='admin_dashboard'),
    # path('admin_login/', views.admin_login, name='admin_login'),
    # path('admin_users',views.admin_users,name='admin_users'),
    # path('user_block/<int:user_id>/', views.user_block, name='user_block'),
    # path('user_unblock/<int:user_id>/',views.user_unblock,name='user_unblock'),
    
    
]