from itertools import product
import json
import re
from django.http import HttpResponse, JsonResponse

from django.http import JsonResponse
from cart.models import Cart
from .models import Order, Profile, Review, Wallet,Transaction
import random
from django.db import IntegrityError
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login
from django.views.decorators.cache import never_cache
from django.contrib.auth import login,logout
from admin_side.models import Coupon, Product, ProductImage
from .utils import send_otp
from datetime import datetime, timedelta
import pyotp
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import PermissionDenied
# Create your views here.
from datetime import date
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from datetime import date

from django.contrib import messages

def home(request):
    products = Product.objects.filter(is_deleted=False, product_quantity__gt=0)

    for product in products:
        if product.product_offer and product.product_offer.end_date >= date.today():
            product.discounted_price = product.product_price - product.product_offer.discount_amount
        else:
            product.discounted_price = None

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None  # or any default value you prefer

    context = {
        'products': products,
        'cart_items': cart_items,
    }

    # Debugging: Output information to the console
    print(f"User: {request.user}, Cart Items: {cart_items}")

    return render(request, 'user_temp/home.html', context)

            
        
    # image=ProductImage.objects.filter(is_delete=False)
    # context = {
    #     'Pro': Pro,
    #     # 'image':image,
    # }
    
    # return render(request, 'user_temp/home.html', context)


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

@login_required
def change_pass(request):
    if request.method == 'POST':
        current_pass = request.POST.get('current_password')
        new_pass = request.POST.get('new_password')
        confirm_new_pass = request.POST.get('confirm_new_password')

        # Verify the old password
        user = authenticate(username=request.user.username, password=current_pass)

        if user is not None:
            # Old password is correct, proceed to change password

            # Password length validation
            if len(new_pass) < 8:
                messages.error(request, 'Password must be at least 8 characters long')
                return render(request, 'user_temp/pass_change.html')

            # Password complexity validation
            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$'
            if not re.match(pattern, new_pass):
                messages.error(request, 'Password must meet complexity requirements')
                return render(request, 'user_temp/pass_change.html')

            # Previous password check
            if user.check_password(new_pass):
                messages.error(request, 'New password cannot be the same as the old password')
                return render(request, 'user_temp/pass_change.html')

            # Check if new passwords match
            if new_pass == confirm_new_pass:
                user.set_password(new_pass)
                user.save()
                update_session_auth_hash(request, user)  # Update the session to prevent the user from being logged out
                messages.success(request, 'Password changed successfully')
                # Redirect to the user profile or another page upon successful password change
                return redirect('user:user_profile')  # Replace 'user:user_profile' with your actual URL name
            else:
                messages.error(request, 'New passwords do not match')
        else:
            messages.error(request, 'Incorrect old password')

    return render(request, 'user_temp/pass_change.html')



from datetime import date

def shop(request):
    # Filter products that are not deleted and have a quantity greater than 0
    products = Product.objects.filter(is_deleted=False, product_quantity__gt=0)

    for product in products:
        if product.product_offer:
            if product.product_offer.end_date >= date.today():
                product.discounted_price = product.product_price - product.product_offer.discount_amount
            else:
                product.discounted_price = None
        else:
            product.discounted_price = None
        if request.user.is_authenticated:
            # Fetch the cart items for the authenticated user
           cart_items = Cart.objects.filter(user=request.user)

    context = {
        'products': products,
        'cart_items':cart_items
    }

    return render(request, 'user_temp/shop_sidebar.html', context)



from datetime import date

def product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_deleted=False,product_quantity__gt=0)
    products = Product.objects.filter(is_deleted=False, product_quantity__gt=0)
    product_images = ProductImage.objects.filter(product=product)
    review = Review.objects.all()
   
    

    # Check for product offer and calculate discounted price
    if product.product_offer and product.product_offer.end_date >= date.today():
        product.discounted_price = product.product_price - product.product_offer.discount_amount
    else:
        product.discounted_price = None
    
    context = {
        'product': product,
        'product_images': product_images,
        'review': review,
        'products':products,
    }
    return render(request, 'user_temp/product_view.html', context)




# def wallet_item(request):
    
#     user_wallets = wallet.objects.filter(user=request.user)

   
#     for user_wallet in user_wallets:
#         print(f"User: {user_wallet.user}, Wallet Amount: {user_wallet.wallet_amount}")

#     context = {
#         'user_wallets': user_wallets,
#     }

#     return render(request, 'user_temp/use_profile.html', context)


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
        ordernote=request.POST.get('ordernote')

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
                streetaddress=street_address,
                town=town,
                state=state,
                phone=phone,
                email=email,
                ordernote=ordernote
            )
            address.save()
            messages.success(request, 'Address Added Successfully')
            # Redirect to a success page

    # Retrieve the user's address data
    user_profile = Profile.objects.filter(user=request.user.id)
    cart_item=Cart.objects.filter(user=request.user)
    # Call the order_history function to get user order history
    user_order = Order.objects.filter(user=request.user).order_by('-created_at')
    order_details = []

    for order in user_order:
        # Get the products associated with the current order
        products = order.product.all()

        # Check if any product in this order has an offer
        has_offer = any(product.product_offer is not None for product in products)

        # order details
        order_detail = {
            'order': order,
            'products': products,
            'has_offer': has_offer,
        }

        order_details.append(order_detail)

    # Retrieve the user's wallet data
    user_wallets = Wallet.objects.filter(user=request.user).prefetch_related('transactions')

    # context with the user's address data, order history, and wallet data
    context = {
        'user_profile': user_profile,
        'user_order': user_order,
        'order_details': order_details,
        'user_wallets':user_wallets,
        'cart_item':cart_item
    }

    return render(request, 'user_temp/user_profile.html', context)


# def edit_profile(adress_id,request):
#     return render(request,'user_temp/edit_profile')






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
        products_in_order = []
        total = 0

        for item in cart:
            total += item.total_price
            products_in_order.append(item.product)

        payment_mode = request.POST.get('payment_method')
        print(payment_mode)
        payment_id = request.POST.get('payment_id')

        if not payment_mode:
            messages.error(request, 'Please choose a payment method')
            return redirect('cart:checkout')

        shipping_cost = 20
        total += shipping_cost

        coupon_code = ''

        if total >= 2000:
            coupon_code = request.POST.get('coupon')

        if coupon_code:
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code, is_deleted=False)
                if total < coupon.min_price:
                    messages.error(request, 'You cannot apply the coupon right now. Shop more and apply it later.')
                    return redirect('cart:checkout')
                total -= coupon.discount
            except Coupon.DoesNotExist:
                messages.error(request, 'Coupon is not valid.')
                return redirect('cart:checkout')

        if payment_mode == 'cash':
            order = Order.objects.create(
                user=user_name,
                payment_mode=payment_mode,
                payment_id=payment_id,
                total_price=total,
                profile=address,
                shipping_cost=shipping_cost,
                od_status='Processing'
            )
           
            for item in cart:
                # Subtract the purchased quantity from the product quantity
                product = item.product
                new_quantity = product.product_quantity - item.quantity

                # Check if the new quantity is valid
                if new_quantity >= 0:
                    product.product_quantity = new_quantity
                    product.save()
                    # Add the product to the order
                    order.product.add(product)
                else:
                    # Handle the case where the product quantity would become negative
                    messages.warning(request, f'Product "{product.product_name}" has insufficient quantity and will not be included in the order.')

            order.save()
            cart.delete()

            messages.success(request, 'Order placed successfully!')

            # Redirect to the checkout.html page
            return render(request, 'user_temp/home.html')

        
        
        elif payment_mode == 'razorpay':
            order = Order.objects.create(
                user=user_name,
                payment_mode=payment_mode,
                total_price=total,
                profile=address,
                shipping_cost=shipping_cost,
                od_status='Processing'
            )

            for item in cart:
                    # Subtract the purchased quantity from the product quantity
                product = item.product
                new_quantity = product.product_quantity - item.quantity

                # Check if the new quantity is valid
                if new_quantity >= 0:
                    product.product_quantity = new_quantity
                    product.save()
                    # Add the product to the order
                    order.product.add(product)
                else:
                    # Handle the case where the product quantity would become negative
                    messages.warning(request, f'Product "{product.product_name}" has insufficient quantity and will not be included in the order.')

            order.save()
            cart.delete()
            messages.success(request, 'Order placed successfully!')

            # Redirect to the checkout.html page
            return render(request, 'user_temp/home.html')

           

            # You can include Razorpay logic here if needed

        elif payment_mode == 'wallet':
            wallet = Wallet.objects.get()
            if wallet.wallet_amount <= total:
                messages.error(request, 'User Wallet Amount won\'t be enough.')
                return redirect('cart:checkout')
            else:
                order = Order.objects.create(
                    user=user_name,
                    payment_mode=payment_mode,
                    payment_id=payment_id,
                    total_price=total,
                    profile=address,
                    shipping_cost=shipping_cost,
                    od_status='Processing'
                )

                for item in cart:
                    # Subtract the purchased quantity from the product quantity
                    product = item.product
                    new_quantity = product.product_quantity - item.quantity

                    # Check if the new quantity is valid
                    if new_quantity >= 0:
                        product.product_quantity = new_quantity
                        product.save()
                        # Add the product to the order
                        order.product.add(product)
                    else:
                        # Handle the case where the product quantity would become negative
                        messages.warning(request, f'Product "{product.product_name}" has insufficient quantity and will not be included in the order.')

            order.save()
            cart.delete()
            
            
            messages.success(request, 'Order placed successfully!')
            return render(request, 'user_temp/order_success.html')

    return redirect('user:home')




def cancel_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)

        allowed_statuses = ['Processing', 'Shipped', 'Pending']

        if order.od_status in allowed_statuses and not order.is_cancelled and order.od_status != 'Return':
            # Update product quantity
            for product in order.product.all():
                try:
                    product.product_quantity += 1  # Assuming the user returns one product
                    product.save()
                except Product.DoesNotExist:
                    # Handle the case where the product does not exist
                    pass

            # Update order status to 'Cancelled'
            order.is_cancelled = True
            order.od_status = 'Cancelled'
            order.save()

            # Add product amount to the user's wallet
            user_wallet, created = Wallet.objects.get_or_create(user=request.user)
            amount_to_add = order.total_price  # Assuming total_price is the product amount
            user_wallet.wallet_amount += amount_to_add
            user_wallet.save()

            # Record the transaction in the wallet history
            transaction = Transaction.objects.create(
                user=request.user,
                amount=amount_to_add,
                transaction_type='credit'
            )
            user_wallet.transactions.add(transaction)

            messages.success(request, 'Order canceled successfully. Amount added to your wallet.')
        else:
            messages.error(request, "This order cannot be canceled.")

    return redirect('user:user_profile')






def track_order(request):
    return render(request,'user_temp/order_track.html')






  
def return_order(request, order_id):
    if request.method=='POST':
        order = Order.objects.get(id=order_id)
        if order.od_status == 'Delivered':
        
            order.od_status = 'Return'
            order.is_cancelled = True
            order.save()
            
            user_wallet,created= Wallet.objects.get_or_create(user=request.user)
            amount_add=order.total_price
            user_wallet.wallet_amount += amount_add
            user_wallet.save()
            
            transaction=Transaction.objects.create(user=request.user,amount=amount_add,transaction_type='credit')
            
            user_wallet.transactions.add(transaction)
            messages.success(request, "Order return successfully . Amount added to your wallet.")  
            
            
        else:
            
            messages.error(request, "This order cannot be canceled.")

    return redirect('user:user_profile')




def wallet_item(request):  
    user_wallets = Wallet.objects.filter(user=request.user)
    context = {
        'user_wallets': user_wallets,
    }

    return render(request, 'user_temp/use_profile.html', context)






def add_review(request, product_id):
    
    product = Product.objects.get(id=product_id)
   
    if request.method == 'POST':
        comment = request.POST.get('comment')
       
       
        user = request.user
       

        
        review = Review(
            user_instance=user,
            product=product,
            comment=comment,
            
            
            
        )
        review.save()
        
       
        return redirect('user:product_view', product_id=product_id)
       

    
    return render(request, 'user_temp/product_view.html')


def success (request):
    return (request,'user_temp/success.html')





def full_order_view(request, order_id):
    # Fetch the specific order based on order_id
    order = Order.objects.filter(user=request.user, id=order_id).first()

    # Check if the order exists
    if order:
        # Check if the product in the order has an offer and calculate the discounted price
        for product in order.product.all():
            if product.product_offer:
                if product.product_offer.end_date >= datetime.now().date():
                    product.discounted_price = product.product_price - product.product_offer.discount_amount
                else:
                    product.discounted_price = None
            else:
                product.discounted_price = None

        context = {
            'order': order
        }
        return render(request, 'user_temp/full_order_view.html', context)
    else:
        # Handle the case where the order doesn't exist (e.g., show an error message)
        return HttpResponse("Order not found.")



@login_required
def edit_address(request, address_id):
  
    
    profile = get_object_or_404(Profile, id=address_id, user=request.user)

    if request.method == 'POST':
       
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        companyname = request.POST.get('companyname')
        country = request.POST.get('country')
        streetaddress = request.POST.get('streetaddress')
        town = request.POST.get('town')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        ordernote = request.POST.get('ordernote')

      
        if not firstname or not lastname or not country or not streetaddress or not town or not state or not phone or not email:
            messages.error(request, 'All fields are required.')
            return render(request, 'user_temp/checkout.html', {'profile': profile})

       
        profile.firstname = firstname
        profile.lastname = lastname
        profile.company_name = companyname
        profile.country = country
        profile.streetaddress = streetaddress
        profile.town = town
        profile.state = state
        profile.phone = phone
        profile.email = email
        profile.ordernote = ordernote
        profile.save()

        
        messages.success(request, 'Address updated successfully.')

       
        return redirect('cart:checkout') 

    return render(request, 'user_temp/checkout.html', {'profile': profile})

