from django.shortcuts import redirect, render
from django.contrib import messages
from admin_side.models import Product
from .models import Cart

# Create your views here.


def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user)
        context={
            'cart':cart
            
        }
     
        return render(request,'user_temp/cart.html',context)
    else:
        messages.error(request,'Please Register Your Account')
        return redirect('user:user_login')
    
  

def add_cart(request, product_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            quantity = '1'
            quantity = int(quantity)
            av_pro = Product.objects.get(id=product_id)

            if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                messages.error(request, 'This Product Is Already Exist In Your Cart')
            else:
                c_obj = Cart.objects.create(user=request.user, product_id=product_id, quantity=quantity)
                c_obj.save()
        return redirect('cart:cart')  # Redirect to the cart page after adding the item
    else:
        messages.error(request, 'Please Register Your Account')
        return redirect('user:user_login')
    
    
def delete_cart(request, cart_id):
    if request.method == 'POST':
        try:
            cart_item = Cart.objects.get(id=cart_id)
            cart_item.delete()
        except Cart.DoesNotExist:
            # Handle the case where the cart item doesn't exist
            pass
        return redirect('cart:cart')
    else:
        return redirect('cart:cart')