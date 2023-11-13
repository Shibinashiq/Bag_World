from admin_side.models import Coupon
from user.models import Profile
from django.db.models import  F
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Sum,ExpressionWrapper,DecimalField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Cart,Wishlist
from decimal import Decimal
from datetime import date


def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).order_by('id')

        if not cart.exists():
            messages.error(request, 'Your cart is empty. Please add items to your cart.')
            return redirect('user:shop') 

        total_price = Decimal(0)  
        shipping_charge = 20  
        for i in cart:
            if i.offer_price is not None:
                A=i.offer_price*i.quantity
            else:
                A=i.product.product_price*i.quantity
            total_price+=A

        grand_total = total_price + shipping_charge
        user_profile=Profile.objects.all()

        context = {
            'cart': cart,
            'shipping_charge': shipping_charge,
            'grand_total': grand_total,
            'total_price': total_price,
            'user_profile':user_profile
        }

        return render(request, 'user_temp/cart.html', context)
    else:
        messages.error(request, 'Please Login')
        return redirect('user:user_login')
    
    
  # Import datetime module


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
            
            # Calculate the offer_price if the product has an offer
            if check_product.product_offer is not None:
                if check_product.product_offer.end_date >= date.today():
                    offer_price = check_product.product_price - check_product.product_offer.discount_amount
                else:
                    offer_price = None  # Offer has expired
            else:
                offer_price = None  # No offer

            # Calculate the total price
            if offer_price is not None:
                total_price = offer_price * product_qty
            else:
                total_price = check_product.product_price * product_qty

            # Create the product in the cart
            if check_product.product_quantity >= int(product_qty):
                cart_obj = Cart.objects.create(
                    user=request.user,
                    product_id=pro_id,
                    quantity=product_qty,
                    total_price=total_price,
                    offer_price=offer_price
                )
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



def update_cart(request, action, product_id):
    
    if request.method == 'POST':
        
        cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
        if cart_item:
            
            if action == "increase":
                if cart_item.product.product_quantity==cart_item.quantity:
                    messages.error(request,'Product out of stock')
            
                else:
                    cart_item.quantity += 1
            
                
            elif action == "decrease":
                if cart_item.quantity>1:
                  cart_item.quantity -= 1
                else:
                      messages.error(request,'you cant order the product below 1')
                    
                # if cart_item.quantity <= 0:
                    # Remove the item from the cart if the quantity becomes zero or less
                    # cart_item.delete()
            else:
                return HttpResponseBadRequest("Invalid action")

            cart_item.total_price = cart_item.product.product_price * cart_item.quantity
            cart_item.save()

            # Calculate the total for the entire cart
            cart_items = Cart.objects.filter(user=request.user)
            cartQnty=cart_item.quantity
            total = sum(item.total_price for item in cart_items)

            status = 'Cart Updated Successfully'
           
            
            response_data = {
                                'success': True,
                                'total': total,
                                'qnty': cartQnty,
                            }

            return JsonResponse(response_data, status=200)
           
        else:
            return HttpResponseBadRequest("Cart item not found")
    else:
        return HttpResponseBadRequest("Invalid request method")
   

     
    
    
    
def delete_cart_item(request,product_id):
    if request.method == 'POST':
        dele = Cart.objects.filter(id = product_id)
   
        dele.delete()
        messages.success(request, 'Successfully Removed')
        return redirect('cart:cart')
    else:
        messages.error(request , 'please login')
        return redirect('user:user_login')
    
    
    
    
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    

    # Check if the cart is empty
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty. Please add items to your cart.')
        return redirect('user:shop')  # Redirect to the shop page if the cart is empty

    user_profile = Profile.objects.filter(user=request.user.id)
    grand_total = 0
    shipping_cost = 20
    for cart_item in cart_items:
            if cart_item.offer_price is not None:
                item_total = cart_item.offer_price * cart_item.quantity
            else:
                item_total = cart_item.product.product_price * cart_item.quantity
            grand_total += item_total

    # Add shipping cost to the grand total
    grand_total += shipping_cost
    available_coupons = Coupon.objects.filter(is_deleted=False)

    context = {
        'cart_items': cart_items,
        'user_profile': user_profile,
        'grand_total': grand_total,
        'available_coupons':available_coupons
    }

    return render(request, 'user_temp/checkout.html', context)







# def multiple_address(request):
#     if request.method == 'POST':
#         # Retrieve the list of addresses submitted in the request
#         addresses = request.POST.getlist('address')
        
#         for address_data in addresses:
#             # Parse the address data
#             first_name = address_data.get('first_name')
#             last_name = address_data.get('last_name')
#             company_name = address_data.get('company_name')
#             country = address_data.get('country')
#             street_address = address_data.get('street_address')
#             town = address_data.get('town')
#             state = address_data.get('state')
#             phone = address_data.get('phone')
#             email = address_data.get('email')

#             # Perform validation for each address
#             if not first_name or not last_name or not email:
#                 messages.error(request, 'Please fill in required fields (First Name, Last Name, Email)')
#             elif len(phone) < 10:
#                 messages.error(request, 'Phone number must be at least 10 digits long')
#             else:
#                 # Data is valid; create a new Profile object and save it
#                 address = Profile(
#                     user=request.user,  # Assuming user is associated with the logged-in user
#                     firstname=first_name,
#                     lastname=last_name,
#                     company_name=company_name,
#                     country=country,
#                     streetaddress=street_address,
#                     town=town,
#                     state=state,
#                     phone=phone,
#                     email=email,
#                 )
#                 address.save()
        
#         messages.success(request, 'Addresses Added Successfully ')
#         return redirect('cart:checkout')  # Redirect to a success page

#     return render(request, 'user_temp/checkout.html')


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




def wishlist_to_cart(request, wishlist_id):
    if request.user.is_authenticated:
        # Get the Wishlist item
        wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)

        # Check if the product is already in the cart
        if Cart.objects.filter(user=request.user, product_id=wishlist_item.product.id).exists():
            messages.error(request, 'Product already exists in the cart')
        else:
            # Check if the product is available in sufficient quantity
            if wishlist_item.product.product_quantity >= 1:
                # Create the product in the cart
                cart_obj = Cart.objects.create(
                    user=request.user,
                    product_id=wishlist_item.product.id,
                    quantity=1,  # You can modify this if needed
                    total_price=wishlist_item.product.product_price
                )
                cart_obj.save()
                messages.success(request, 'Product added to cart successfully')
                return redirect ('cart:cart')
            else:
                messages.error(request, 'Product is out of stock')

        # Delete the item from the wishlist
        wishlist_item.delete()
    else:
        messages.error(request, 'Please log in')
    
    return redirect('cart:wishlist')


# import random
# import string
# from django.http import JsonResponse


# def generate_coupon(request):
#     # if request.method == 'POST':
#         if request.user.is_authenticated:
#             # Generate a random 4-digit coupon code
#             coupon_code = ''.join(random.choices(string.digits, k=4))
#             request.session['coupon_code'] = coupon_code

#             # Print for debugging
           

#             return JsonResponse({'coupon_code': coupon_code})
#         else:
#             # Handle the case where the user is not authenticated
#             return JsonResponse({'error': 'Please log in to get a coupon.'})
   
    

# from decimal import Decimal

# # ...
# import json
# from decimal import Decimal

# # ...

# from decimal import Decimal

# def apply_and_display_coupon(request):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             user_entered = request.POST.get('coupon')
#             coupon_code = request.session.get('coupon_code')
#             if coupon_code and user_entered == coupon_code:
#                 # Generate a random 3-digit discount code
#                 discount_code = ''.join(random.choices(string.digits, k=3))
#                 request.session['discount_code'] = discount_code

#                 # Calculate the total_price (subtotal) and discount_amount
#                 user_cart = Cart.objects.filter(user=request.user)
#                 total_price = user_cart.aggregate(total_price=Sum(F('total_price')))['total_price'] or Decimal('0.00')
                
#                 discount_amount = Decimal(discount_code)  # Assuming the discount code directly represents the discount amount
#                 shipping_coast=20
#                 # Calculate the new grand total after applying the discount
#                 grand_total = total_price + shipping_coast - discount_amount 
        


#                 # Convert Decimal to a serializable format (e.g., float)
#                 grand_total_serializable = float(grand_total)

#                 request.session['discounted_total'] = grand_total_serializable
                
                
#                 messages.success(request, f'Coupon code applied successfully. You received a discount of {discount_amount}.')
#                 return redirect('cart:cart')
#             else:
#                 messages.error(request, 'Invalid coupon code')
#                 return redirect('cart:cart')
#         else:
#             messages.error(request, 'Please log in to apply a coupon.')
#             return redirect('user:user_login')
#     else:
#         return render(request, 'user_temp/cart.html')


