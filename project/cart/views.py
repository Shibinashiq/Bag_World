# views.py
import decimal
from user.models import Profile
from django.db.models import ExpressionWrapper, F, FloatField
from django.forms import DecimalField, FloatField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, Wishlist
from django.contrib import messages
from admin_side.models import  Product, ProductImage
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Cart
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from django.db.models import Sum

def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).order_by('id')

        # Check if the cart is empty
        if not cart.exists():
            messages.error(request, 'Your cart is empty. Please add items to your cart.')
            return redirect('user:shop')  # Redirect to the shop or another appropriate page
        # eligible_for_coupon = grand_total > 2000
        total_price = cart.aggregate(total=Sum(F('product__product_price') * F('quantity')))['total'] or 0
        shipping_charge = 10  # Set your shipping charge here
        grand_total = total_price + shipping_charge

        context = {
            'cart': cart,
            'shipping_charge': shipping_charge,
            'grand_total': grand_total,
            'total_price': total_price,
            
        }

        return render(request, 'user_temp/cart.html', context)
    else:
        messages.error(request, 'Please Login')
        return redirect('user:user_login')

def add_cart(request):
  
    if request.method == 'POST':
        if request.user.is_authenticated:

            pro_id = request.POST.get('product_id')
            quantity = int(request.POST.get('product_count'))

            # Validation
            try:
                check_product = Product.objects.get(id=pro_id)
            except Product.DoesNotExist:
                messages.error(request, 'Product does not exist')
                return redirect('user:shop')

            # Check if the product is already in the cart
            if Cart.objects.filter(user=request.user, product_id=pro_id).exists():
                messages.error(request, 'Product already exists in the cart')
                return redirect('cart:cart')
            else:
                product_qty = quantity

                # Create the product in the cart
                if check_product.product_quantity >= int(product_qty):
                    product_price = check_product.product_price
                    total_price = product_price * product_qty

                    cart_obj = Cart.objects.create(user=request.user, product_id=pro_id, quantity=product_qty, total_price=total_price)
                    cart_obj.save()
                    messages.success(request, 'Product Added Successfully')
                    return redirect('cart:cart')
                else:
                    messages.error(request, 'Only a few quantities available')
                    return redirect('user:shop')
        else:
            messages.error(request, 'Please log in')
            return redirect('user:user_login')

    return render(request, 'user_temp/cart.html')

from django.http import JsonResponse
from django.shortcuts import redirect
from decimal import Decimal  # Import Decimal for precise decimal calculations

def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        product_qty = int(request.POST.get('quantity'))

        # Initialize sub_total
        sub_total = 0
        total=0
        # Check if the product exists in the user's cart
        cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
        if cart_item:
            if product_qty == 0:
                # Prevent adding zero quantity items
                status = 'zero qty not allowed'
            elif product_qty > cart_item.product.product_quantity:
                # Check if the requested quantity exceeds available quantity
                status = 'Requested quantity exceeds available quantity'
            else:
                # Update the quantity in the cart
                cart_item.quantity = product_qty
                cart_item.save()

                # Calculate the single item price
                product_price = cart_item.product.product_price
                brand_offer = cart_item.product.product_brand.offer
                product_offer = cart_item.product.offer

                if product_offer and brand_offer:
                    max_discount = max(product_offer.discount_amount, brand_offer.discount_amount)
                elif product_offer:
                    max_discount = product_offer.discount_amount
                elif brand_offer:
                    max_discount = brand_offer.discount_amount
                else:
                    max_discount = 0

                discount = Decimal((max_discount / 100) * product_price)
                discount_price = product_price - discount
                sub_total = discount_price * cart_item.quantity

                # Update total price in the cart
                cart_items = Cart.objects.filter(product_id=product_id, user=request.user)
                grand_total = {}
                for item in cart_items:
                    if action == 'increment':
                        item.total_price += Decimal(sub_total)
                    elif action == 'decrement':
                        item.total_price -= Decimal(sub_total)
                    item.save()
                    grand_total[item.id] = item.total_price
                max_id = max(grand_total)
                total = grand_total[max_id]

                status = 'Cart Updated Successfully'
        else:
            status = 'No matching product found in cart'

        return JsonResponse({'status': status, 'sub_total': sub_total, 'total': total})

    else:
        return redirect('cart')


def delete_cart(request,delete_id):
    if request.method == 'POST':
        dele = Cart.objects.filter(id = delete_id)
   
        dele.delete()
        messages.success(request, 'Successfully Removed')
        return redirect('cart:cart')
    else:
        messages.error(request , 'please login')
        return redirect('user:user_login')
    
    
    
    
    
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    user_profile = Profile.objects.filter(user=request.user.id)
    context = {
        'cart_items': cart_items,
        'user_profile':user_profile
        
    }

    return render(request, 'user_temp/checkout.html', context)




def multiple_address(request):
    if request.method == 'POST':
        # Retrieve the list of addresses submitted in the request
        addresses = request.POST.getlist('address')
        
        for address_data in addresses:
            # Parse the address data
            first_name = address_data.get('first_name')
            last_name = address_data.get('last_name')
            company_name = address_data.get('company_name')
            country = address_data.get('country')
            street_address = address_data.get('street_address')
            town = address_data.get('town')
            state = address_data.get('state')
            phone = address_data.get('phone')
            email = address_data.get('email')

            # Perform validation for each address
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
                    email=email
                )
                address.save()
        
        messages.success(request, 'Addresses Added Successfully ')
        return redirect('cart:checkout')  # Redirect to a success page

    return render(request, 'user_temp/checkout.html')


def wishlist(request):
    list = Wishlist.objects.filter(user=request.user).order_by('created_at')
    
    context = {
        'list': list
    }
    
    return render(request, 'user_temp/wishlist.html', context)



def add_wishlist(request, product_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                pro_id = Product.objects.get(id=product_id)
                # Check if the product is already in the user's wishlist
                if Wishlist.objects.filter(user=request.user, product=pro_id).exists():
                    messages.warning(request, 'This product is already in your wishlist.')
                    return redirect('cart:wishlist')
                else:
                    Wishlist.objects.create(user=request.user, product=pro_id)
                    messages.success(request, 'Product added to your wishlist.')
                    return redirect('cart:wishlist')
            except Product.DoesNotExist:
                messages.error(request, 'Product not found.')
        else:
            messages.error(request, 'Please log in to add products to your wishlist.')
            return redirect('user:user_login')
    return render(request, 'user_temp/wishlist.html')

def remove_wishlist(request, product_id):
    if request.user.is_authenticated:
        # Use get_object_or_404 to get the Wishlist item or return a 404 if it doesn't exist
        item = get_object_or_404(Wishlist, id=product_id, user=request.user)
        item.delete()  # Remove the item from the wishlist
        messages.success(request,'Item Removed ')
    return redirect('cart:wishlist') 




import random

# Define the length of the coupon code
code_length = 4 # You can adjust this to your desired length

# Generate a random coupon code containing numbers only
def generate_coupon_code(length):
    coupon_code = ''.join(str(random.randint(0, 9)) for _ in range(length))
    return coupon_code

# Generate and print a random coupon code
coupon = generate_coupon_code(code_length)
print("Random Coupon Code:", coupon)