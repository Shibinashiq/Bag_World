from itertools import product
from cart.models import Cart
from .models import Order, Profile
import random
from django.db import IntegrityError
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login
from django.views.decorators.cache import never_cache
from django.contrib.auth import login,logout
from admin_side.models import Product, ProductImage
from .utils import send_otp
from datetime import datetime, timedelta
import pyotp
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def home(request):
    # Filter products that are not deleted
    Pro = Product.objects.filter(is_deleted=False)
    # image=ProductImage.objects.filter(is_delete=False)
    context = {
        'Pro': Pro,
        # 'image':image,
    }
    
    return render(request, 'user_temp/home.html', context)


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
    # Filter products that are not deleted
    products = Product.objects.filter(is_deleted=False)
    context = {
        'products': products
    }

    return render(request, 'user_temp/shop.html', context)



def user_profile(request):
    if request.method == 'POST':
        # Retrieve data from the request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        country = request.POST.get('country')
        street_address = request.POST.get('street_address')
        town = request.POST.get('town')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Perform validation here
        if not first_name or not last_name or not email:
            messages.error(request, 'Please fill in required fields (First Name, Last Name, Email)')
        elif len(phone) < 10:
            messages.error(request, 'Phone number must be at least 10 digits long')
        else:
            # Data is valid; create a new Profile object and save it
            address = Profile(
                user=request.user,  # Assuming user is associated with the logged-in user
                firstname=first_name,
                lastname=last_name,
                company_name=company_name,
                country=country,
                street_address=street_address,
                town=town,
                state=state,
                phone=phone,
                email=email
            )
            address.save()
            messages.success(request, 'Address Added Successfully ')
            return redirect('user:user_profile')  # Redirect to a success page

    # Retrieve the user's address data, assuming you have a user profile
    user_profile = Profile.objects.filter(user=request.user.id)

    # Call the order_history function to get user order history
    user_order= Order.objects.filter(user=request.user).order_by('-created_at')
    order_details = []

    for order in user_order:
        # Get the products associated with the current order
        products = order.product.all()
        
        # Create a dictionary to store order details
        order_detail = {
            'order': order,
            'products': products,
        }

        order_details.append(order_detail)
    # Prepare the context with the user's address data and order history
    context = {
        'user_profile': user_profile,
        'user_order': user_order
    }

    return render(request, 'user_temp/user_profile.html', context)


def edit_address(request, address_id):
    
    edit = get_object_or_404(Profile, id=address_id, user=request.user)

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

        # Validations
        if not first_name or not last_name or not email:
            messages.error(request, 'Please fill in required fields (First Name, Last Name, Email)')
            return redirect('edit_address', address_id=address_id)

        if len(phone) < 10:
            messages.error(request, 'Phone number must be at least 10 digits long')
            return redirect('edit_address', address_id=address_id)

        # Update the address fields
        edit.first_name = first_name
        edit.last_name = last_name
        edit.company_name = company_name
        edit.country = country
        edit.streetaddress = street_address
        edit.town = town
        edit.state = state
        edit.phone = phone
        edit.email = email
        edit.save()
        messages.success(request, 'Address Edited Successfully')

        # Redirect to a success page or another appropriate page
        return render(request, 'user_temp/userprofile.html')

    context = {'edit_address': edit}
    return render(request, 'user_temp/user_profile.html', context)



def place_order(request):
    if request.method == 'POST':
        user = request.user
        user_name = User.objects.get(username=user)
        address_id = request.POST.get('address_id')


        if address_id is None:
            messages.error(request, 'Address should be provided')
            return redirect('cart:checkout')
        cart = Cart.objects.filter(user=request.user)
        address = Profile.objects.get(id=address_id)
        # product = Product.objects.filter(id=product_id)
        products_in_order = []  # List to store products in the order
        total = 0
        for item in cart:
            total += item.total_price
            # Add the product to the list of products in the order
            products_in_order.append(item.product)


        payment_mode = request.POST.get('payment-method')
        payment_id = request.POST.get('payment_id')




#     return render(request, 'user_temp/user_profile.html')
        for item in cart:
            total += item.total_price
        print('the total price is the ',total)
        # Create an order object and save it to the database
        order = Order.objects.create(
            user=user_name,
            payment_mode=payment_mode,
            payment_id=payment_id,
            total_price= total,
            profile = address,
            # product=product,
        )

        for item in cart:
            order.product.add(item.product)


        order.save()
        order.product.set(products_in_order)

        cart.delete()

        # Here, you might want to handle the payment if applicable.

        return redirect( 'user:place_order')


    return render(request, 'user_temp/order_success.html')


from django.core.exceptions import PermissionDenied

def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.od_status == 'Pending':
            order.is_cancelled = True
            order.save()
            # Optionally, you can add logic for order cancellation confirmation or notifications.
        else:
            # Handle cases where the order cannot be canceled.
            raise PermissionDenied("This order cannot be canceled.")
    except Order.DoesNotExist:
        # Handle the case where the order doesn't exist.
        pass  # You can add specific error-handling logic here if needed.
    return redirect('user:order_history')
