# views.py
import decimal
from user.models import Profile
from django.db.models import ExpressionWrapper, F, FloatField
from django.forms import DecimalField, FloatField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart
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
        # cart_image = ProductImage.objects.filter(is_available=True).first()

        # Calculate the total price using Sum
        total_price = cart.aggregate(total=Sum(F('product__product_price') * F('quantity')))['total'] or 0

        shipping_charge = 10  # Set your shipping charge here

        grand_total = total_price + shipping_charge
        total_price = 0  # Initialize the total price to zero

        # for item in cart:
        #     total_pro_price += item.product.product_price * item.quantity

        
        context = {
            'cart': cart,
            # 'cart_image': cart_image,
            # 'totalprice': totalprice,
            'shipping_charge': shipping_charge,
            'grand_total': grand_total,
            'total_price' :total_price
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
                single_price = discount_price * cart_item.quantity

                # Update total price in the cart
                cart_items = Cart.objects.filter(product_id=product_id, user=request.user)
                grand_total = {}
                for item in cart_items:
                    if action == 'increment':
                        item.total_price += Decimal(single_price)
                    elif action == 'decrement':
                        item.total_price -= Decimal(single_price)
                    item.save()
                    grand_total[item.id] = item.total_price
                max_id = max(grand_total)
                total = grand_total[max_id]

                status = 'Cart Updated Successfully'
        else:
            status = 'No matching product found in cart'

        return JsonResponse({'status': status, 'single_price': single_price, 'total': total})

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
def multiple_address (request):
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
        print(address)
        address.save()

        messages.success(request, 'Address Added Successfully ')
    return render (request,'user_temp/checkout.html')



