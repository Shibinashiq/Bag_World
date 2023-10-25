from .models import Profile
import random
from django.db import IntegrityError
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login
from django.views.decorators.cache import never_cache
from django.contrib.auth import login,logout
from admin_side.models import Product
from .utils import send_otp
from datetime import datetime, timedelta
import pyotp
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def home(request):
    
    return render(request,'user_temp\home.html')

def user_login(request):
 if request.method=='POST':
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(username=username,password=password)
    if user is not None:
        login(request,user)
        # messages.success(request,f'welcome back {username}successfully logged in')
        return redirect('user:home')
    else:
        messages.error(request,'Bad credential please try again ')
        return redirect('user:user_login')
    
 return render(request,'user_temp/login.html')

def user_signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if User.objects.filter(username=username).exists():
            messages.error(request,'User is exists')
            return redirect('user:user_signup')
        if User.objects.filter(email=email).exists():
            messages.error(request,'email already taken')
            return redirect('user:user_signup')
        
        if password==confirm_password:
            
            request.session['username']=username
            request.session['email']=email
            request.session['password']=password
            # user=User.objects.create(username=username,email=email,password=password)
            send_otp(request, email)
            return redirect('user:otp')
        else:
            messages.error(request, 'Password do not match')

 
    return render(request,'user_temp/signup.html')
    
    
    
def otp_page(request):
    error_message = None
    if request.method == 'POST':
        otp = request.POST['otp']
        import pdb
        pdb.set_trace()
        username = request.session['username']  
        otp_secret_key = request.session['otp_secret_key']  # Use square brackets here
        otp_valid_until = request.session['otp_valid_date']  # Use square brackets here
        
        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    
                    username=request.session['username']
                    password=request.session['password']
                    email=request.session['email']
                    
                    # if email is not None and otp_secret_key is not None and otp_valid_until is not None:
                    user = User.objects.create(username=username, email=email, password=make_password(password))
                    user.save()
                    login(request, user)
                    import pdb
                    pdb.set_trace()
                    if request.session['username']:
                        del request.session['username']
                        del request.session['password']
                        del request.session['email']
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                    return redirect('user:home')
                else:
                    error_message='invalid OTP'
            else:
               error_message='OTP expired'
        else:
            error_message='Oops,something went wrong'
    return render(request, 'user_temp/otp.html', {'error_message':error_message})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('user:home')


def shop(request):
    
    product=Product.objects.all()
    for i in product:
        if i.product_image:
            print(i.product_image.url)
    context={
        'product':product
    }
    return render (request, 'user_temp/shop.html',context)


# def user_address(request):
#     if request.method == 'POST':
#     # Retrieve the user's address data, assuming you have a user profile
#         user_profile = Profile.objects.filter(user=request.user.id)
#         print(user_profile)
#         # Prepare the context with the user's address data
#         context = {
#             'user_profile': user_profile
#         }

#     return render(request, 'user_temp/user_profile.html', context)
def user_profile(request):
    if request.method == 'POST':
        # Handle address update
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        country = request.POST.get('country')
        street_address = request.POST.get('street_address')
        town = request.POST.get('town')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Create a new Profile object
        address = Profile(
            user=request.user,  # Assuming user is associated with the logged-in user
            firstname=first_name,
            lastname=last_name,
            company_name=company_name,
            country=country,
            streetaddress=street_address,
            town=town,
            state=state,
            phone=phone,
            email=email
        )
        address.save()

        messages.success(request, 'Address Added Successfully ')

        # Redirect to a success page or the same page

    # Retrieve the user's address data, assuming you have a user profile
    user_profile = Profile.objects.filter(user=request.user.id)

    # Prepare the context with the user's address data
    context = {
        'user_profile': user_profile
    }

    return render(request, 'user_temp/user_profile.html', context)


# def edit_address(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         company_name = request.POST.get('company_name')
#         country = request.POST.get('country')
#         street_address = request.POST.get('street_address')
#         town = request.POST.get('town')
#         state = request.POST.get('state')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
        
        
#         edit= Profile.objects.filter(user=request.user.id)
        
#         edit.first_name=first_name
#         edit.last_name=last_name
#         edit.company_name=company_name
#         edit.country=country
#         edit.street_address=street_address
#         edit.town=town
#         edit.state=state
#         edit.phone=phone
#         edit.email=email
#         edit.save()
#         messages.success(request, 'Address Edited Successfully ')

#         # Redirect to a success page
       

#     return render(request, 'user_temp/user_profile.html')




def order_success(request):
    return render (request,'user_temp/order_success.html')