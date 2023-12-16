from django.urls import path
from . import views
app_name='chat'

urlpatterns = [ 
    path('mychat/', views.chatpage, name='chatpage'),
    path('admin_chat', views.admin_chat, name='admin_chat'),

    path('admin_chatpage/<int:user_id>/', views.admin_chatpage, name='admin_chatpage'),
    # path('admin_chat/<int:thread_id>/<str:recipient_id>/', views.admin_chat, name='admin_chat'),
    path('get_messages/<str:thread_name>/', views.get_messages, name='get_messages'),
]