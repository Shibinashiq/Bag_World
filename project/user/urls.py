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
    
    
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('place_order/', views.place_order, name='place_order'),
    
    

    # path('user_address',views.user_address, name='user_address'),
    # path('edit_address/<int:user_id>/',views.edit_address, name='edit_address'),
    
    
    
    # path('contact',views.contact,name='contact'),
    # path('blog',views.contact,name='blog.html'),
    # path('about_us',views.about_us,name='about_us.html'),
    # path('contact_page',views.contact_page,name='contact_page.html'),
   
    
    
    # path('admin_dashboard.html', views.admin_dashboard, name='admin_dashboard'),
    # path('admin_login/', views.admin_login, name='admin_login'),
    # path('admin_users',views.admin_users,name='admin_users'),
    # path('user_block/<int:user_id>/', views.user_block, name='user_block'),
    # path('user_unblock/<int:user_id>/',views.user_unblock,name='user_unblock'),
    
    
]