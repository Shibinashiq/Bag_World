from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Message
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404



@login_required(login_url='user:user_signup')

def chatpage(request):
    user = request.user
    # print(user.id)  # Add this line for debugging
    
    user_messages = Message.objects.filter(sender=user).order_by('timestamp')
    # print(user_messages)  

    context = {
        'user_messages': user_messages,
    }
    return render(request, 'user_temp/chatpage.html', context)


@login_required
def admin_chat(request):
    user_id = request.user.id
    context={
        'user_id':user_id
    }
    return render(request, 'admin_temp/admin_chat.html',context)

@login_required
def admin_chatpage(request, user_id):
   
    user = get_object_or_404(User, id=user_id)

    # Fetch messages for the thread
    thread_name = f"user_{request.user.id}_{user.id}"
    messages = Message.objects.filter(thread_name=thread_name).order_by('timestamp')

    context = {
        'user': user,
        'user_messages': messages,
    }

    return render(request, 'admin_temp/admin_chat_messages.html', context)


# def admin_chatpage(request):
#     # Retrieve threads associated with the current user (admin)
#     threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread')
#     context = {
#         'Threads': threads,
#     }
#     return render(request, 'admin_side/admin_chat.html', context)

# def admin_chat(request, thread_id, recipient_id):
#     # Retrieve the thread and recipient user based on thread_id and recipient_id
    
#     thread = get_object_or_404(Thread, id=thread_id, admin=request.user)
#     recipient_user = get_object_or_404(User, username=recipient_id)
    
#     # Retrieve old messages for the thread
#     old_messages = ChatMessage.objects.filter(thread=thread).order_by('timestamp')
#     context = {
#         'Thread': thread,
#         'RecipientUser': recipient_user,
#         'old_messages': old_messages,
#     }
#     return render(request, 'admin_side/admin_chat_messages.html', context)


# views.py

from django.http import JsonResponse

def get_messages(request, thread_name):
    messages = Message.objects.filter(thread_name=thread_name)
    messages_data = [{'sender_username': msg.sender_username, 'message': msg.message, 'timestamp': msg.timestamp} for msg in messages]
    return JsonResponse({'messages': messages_data})
