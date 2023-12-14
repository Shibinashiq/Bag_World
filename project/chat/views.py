from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Message
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404



@login_required(login_url='user:user_signup')
def chatpage(request):
#     user = request.user  # Get the authenticated user

#     try:
#         admin = User.objects.filter(is_superuser=True).first()
#     except User.DoesNotExist:
#         # Handle the case where no superuser is found
#         raise Http404("No superuser found")

#     # Rest of your code...
    
#     # Check if a thread exists between the user and admin
#     thread = Thread.objects.filter(first_person=user, admin=admin).first()
#     old_messages = ChatMessage.objects.filter(thread=thread).order_by('timestamp') if thread else None

#     context = {
#         'user': user,
#         'old_messages': old_messages,
#     }
    return render(request, 'user_temp/chatpage.html')



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