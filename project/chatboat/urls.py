from django.urls import path
from . import views

app_name='chatboat'

    
urlpatterns = [
    
    path('chat/', views.chat, name='chat'),
    
]