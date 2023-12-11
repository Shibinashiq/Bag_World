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
from django.contrib.auth.decorators import login_required

@login_required(login_url='user:user_login')
def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).order_by('id')

        if not cart.exists():
            messages.error(request, 'Your cart is empty. Please add items to your cart.')
            return redirect('user:shop') 

        product_total_price = Decimal(0) 
        
        shipping_charge = 20  
        for i in cart:
            if i.offer_price is not None:
                A=i.offer_price*i.quantity
            else:
                A=i.product.product_price*i.quantity
            product_total_price+=A
         
        
        grand_total = product_total_price + shipping_charge
        user_profile=Profile.objects.all()
        
        print(grand_total)
        context = {
            'cart': cart,
            'shipping_charge': shipping_charge,
            'grand_total': grand_total,
            'total_price': product_total_price,
            'user_profile':user_profile
        }

        return render(request, 'user_temp/cart.html', context)
    else:
        messages.error(request, 'Please Login')
        return redirect('user:user_login')
    
    
  # Import datetime module

@login_required(login_url='user:user_login')
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
                return redirect('user:shop')
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
            if check_product.product_quantity <= 0 or check_product.is_deleted:
                    messages.error(request, 'Product is not available')
                    return redirect('user:shop')
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
                return redirect('user:shop')
            else:
                messages.error(request, 'Only a few quantities available')
                return redirect('user:shop')
        else:
            messages.error(request, 'Please log in')
            return redirect('user:user_login')
           
    return render(request, 'user_temp/cart.html')

# @login_required(login_url='user:user_login')
def update_cart(request, action, product_id):
    if request.method == 'POST':
        cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
        if cart_item:
            # Check if the product has an offer
            offer_price = None
            if cart_item.product.product_offer is not None:
                if cart_item.product.product_offer.end_date >= date.today():
                    offer_price = cart_item.product.product_price - cart_item.product.product_offer.discount_amount
            
            if action == "increase":
                if cart_item.product.product_quantity == cart_item.quantity:
                    response_data = {
                        'success': False,
                        'error': 'Product out of stock',
                    }
                    return JsonResponse(response_data, status=400)
                else:
                    cart_item.quantity += 1
            elif action == "decrease":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                else:
                    response_data = {
                        'success': False,
                        'error': 'Minimum quantity should be 1',
                    }
                    return JsonResponse(response_data, status=400)
            else:
                return HttpResponseBadRequest("Invalid action")
            
            # Update the total_price based on offer_price or regular price
            if offer_price is not None:
                cart_item.total_price = offer_price * cart_item.quantity
            else:
                cart_item.total_price = cart_item.product.product_price * cart_item.quantity

            cart_item.save()

            # Calculate the total for the entire cart
            cart_items = Cart.objects.filter(user=request.user)
            cartQnty = cart_item.quantity
            total = sum(item.total_price for item in cart_items)

            status = 'Cart Updated Successfully'

            response_data = {
                'success': True,
                'total': total,
                'qnty': cartQnty,
                'productId': product_id,
                'subTotal': cart_item.total_price
            }

            return JsonResponse(response_data, status=200)
        else:
            return HttpResponseBadRequest("Cart item not found")
    else:
        return HttpResponseBadRequest("Invalid request method")

   

     
    
    
@login_required(login_url='user:user_login')    
def delete_cart_item(request,product_id):
    if request.method == 'POST':
        dele = Cart.objects.filter(id = product_id)
   
        dele.delete()
        messages.success(request, 'Product Deleted .')
        return redirect('cart:cart')
    else:
        messages.error(request ,'please login')
        return redirect('user:user_login')
    
    
    
@login_required(login_url='user:user_login')    
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    # Check if the cart is empty
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty. Please add items to your cart.')
        return redirect('user:shop')  # Redirect to the shop page if the cart is empty

    user_profile = Profile.objects.filter(user=request.user.id)
    grand_total = 0
    shipping_cost = 20
    available_cart_items = []

    for cart_item in cart_items:
        if cart_item.product.product_quantity > 0 and not cart_item.product.is_deleted:
            # Product is available, add to the list
            available_cart_items.append(cart_item)

            if cart_item.offer_price is not None:
                item_total = cart_item.offer_price * cart_item.quantity
            else:
                item_total = cart_item.product.product_price * cart_item.quantity
            grand_total += item_total

    # Check if there are any available items in the cart
    if not available_cart_items:
        messages.error(request, 'All products in your cart are not available for checkout.Please wait some days we will inform You')
        return redirect('cart:cart')

    # Add shipping cost to the grand total
    grand_total += shipping_cost
    available_coupons = Coupon.objects.filter(is_deleted=False)

    context = {
        'cart_items': available_cart_items,
        'user_profile': user_profile,
        'grand_total': grand_total,
        'available_coupons': available_coupons
    }

    return render(request, 'user_temp/checkout.html', context)

@login_required(login_url='user:user_login')
def wishlist(request):
    list = Wishlist.objects.filter(user=request.user).order_by('created_at')
    cart_item=Cart.objects.filter(user=request.user)
    
    
    context = {
        'list': list,
        'cart_item':cart_item
    }
    
    return render(request, 'user_temp/wishlist.html', context)


@login_required(login_url='user:user_login')
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
                    wishlist_item = Wishlist.objects.create(user=request.user, product=pro_id)
                
                    if pro_id.product_offer is not None and pro_id.product_offer.end_date >= date.today():
                        # Calculate the discounted price and assign it to the wishlist_item
                        discounted_price = pro_id.product_price - pro_id.product_offer.discount_amount
                        wishlist_item.offer_price = discounted_price
                        print(wishlist_item.offer_price)
                    else:
                        # If there's no offer, leave the price field as it is (you can set a default value if needed)
                        pass
                    
                    # Save the wishlist_item after setting the price
                    wishlist_item.save()

                    messages.success(request, 'Product added to your wishlist.')
                    return redirect('cart:wishlist')
            except Product.DoesNotExist:
                messages.error(request, 'Product not found.')
        else:
            messages.error(request, 'Please log in to add products to your wishlist.')
            return redirect('user:user_login')
    return render(request, 'user_temp/wishlist.html')




@login_required(login_url='user:user_login')
def remove_wishlist(request, product_id):
    if request.user.is_authenticated:
        # Use get_object_or_404 to get the Wishlist item or return a 404 if it doesn't exist
        item = get_object_or_404(Wishlist, id=product_id, user=request.user)
        item.delete()  # Remove the item from the wishlist
        messages.success(request,'Item Removed ')
    return redirect('cart:wishlist') 



@login_required(login_url='user:user_login')
def wishlist_to_cart(request, wishlist_id):
    if request.user.is_authenticated:
        # Get the Wishlist item
        wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)

        # Check if the product is already in the cart
        if Cart.objects.filter(user=request.user, product_id=wishlist_item.product.id).exists():
            messages.error(request, 'Product already exists in the cart')
            return redirect('cart:cart')
        else:
            check_product = wishlist_item.product

            # Check if the product quantity is available and the product is not deleted
            if check_product.product_quantity > 0 and not check_product.is_deleted:
                # Use offer price if available, otherwise use the regular product price
                cart_price = wishlist_item.offer_price if wishlist_item.offer_price else wishlist_item.product.product_price

                # Create the product in the cart
                cart_obj = Cart.objects.create(
                    user=request.user,
                    product_id=wishlist_item.product.id,
                    quantity=1,  # You can modify this if needed
                    total_price=cart_price,
                    offer_price=cart_price,
                )

                wishlist_item.delete()
                cart_obj.save()

                messages.success(request, 'Product added to cart successfully')
                return redirect('cart:cart')
            else:
                messages.error(request, 'Product is not available')
                return redirect('user:home')

    else:
        messages.error(request, 'Please log in')
        return redirect('cart:wishlist')

