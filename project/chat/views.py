from django.shortcuts import render


def chatpage(request):
    return render(request,'user_temp/chatpage.html')