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

    # Retrieve the user instance from the database
    user_instance = User.objects.get(id=user_id)

    # Now you can access the user_name attribute
    user_name = user_instance.username

    # Retrieve messages where the admin is the sender and the user is the recipient
    admin_messages = Message.objects.filter(sender=request.user, sender_username=user_name)

    context = {
        'user_id': user_id,
        'user_name': user_name,
        'admin_messages': admin_messages,  # Add this to the context
    }

    print(admin_messages)  # This will print the user_name to the console

    return render(request, 'admin_temp/admin_chat.html', context)



from django.http import JsonResponse

def get_messages(request, thread_name):
    messages = Message.objects.filter(thread_name=thread_name)
    messages_data = [{'sender_username': msg.sender_username, 'message': msg.message, 'timestamp': msg.timestamp} for msg in messages]
    return JsonResponse({'messages': messages_data})
