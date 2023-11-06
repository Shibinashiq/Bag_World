from decimal import Decimal, InvalidOperation
import re
from django.contrib.auth import authenticate,login
from django.db.models import Q
from django.shortcuts import redirect, render , get_object_or_404

from user.models import Order
from .models import Brand, Offer, ProductImage
from .models import Category
from .models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout


@login_required(login_url='admin_side:admin_login')    
def admin_dashboard(request):
    return render(request,'admin_temp/dashboard.html')


@login_required(login_url='admin_side:admin_login')   
def admin_login(request):
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None and user.is_superuser:
            login(request,user)
            return redirect('admin_side:admin_dashboard')
        else:
            messages.error(request,'Invalid User Try Again')
            return redirect('admin_side:admin_login')
    
    return render(request,'admin_temp/admin_login.html')

@login_required(login_url='admin_side:admin_login')   
def admin_logout(request):
    logout(request)
    # Redirect to the admin login page after logging out.
    return redirect('admin_side:admin_login')

# def admin_users(request):
#     return render(request,'admin_users.html')

# def add_product(request):
#    return render(request,'admin_temp/add-product.html')

def brand(request):
    brand = Brand.objects.all()
    context = {
        'brand':brand
    }
    return render(request,'admin_temp/brand.html',context)

@login_required(login_url='admin_side:admin_login')   
def add_brand(request):
    if request.user.is_superuser:
        if request.method=='POST':
            Brand_name=request.POST.get('brand_name')
            Brand_image=request.FILES.get('brand_image')
            if Brand_name.strip() == '':
                messages.error(request,'Fill In The Field') 
                return redirect('admin_side:brand')  
            
            if Brand_image is None:
                messages.error(request,'Image fields is None')
                return redirect('admin_side:brand')

                
            if Brand.objects.filter(brand_name=Brand_name).exists():
                messages.error(request,'The Brand Name is Already taken')
                return  redirect('admin_side:brand')
            if Brand.objects.filter(brand_image=Brand_image).exists():
                messages.error(request,'Brand Image Is Exist')
                return redirect('admin_side:brand')
            if not re.search(r'[a-zA-Z]', Brand_name):
                messages.error(request, 'Brand Name must contain both letters and not only numbers. Please try again.')
                return redirect('admin_side:brand')

            
            new_brand=Brand(
                brand_name=Brand_name,
                brand_image=Brand_image,
            )
            new_brand.save()
            return redirect ('admin_side:brand')
        return render(request,'admin_temp/add_brand.html')
    else:
        return redirect('admin_login')
        
        
@login_required(login_url='admin_side:admin_login')     
def edit_brand(request, brand_id):
   if request.user.is_superuser:
        if request.method == 'POST':
            Brand_name = request.POST.get('brand_name')
            Brand_image = request.FILES.get('brand_image')
            bra = Brand.objects.get(id=brand_id)

            # Check if Brand_name is empty
            if not Brand_name.strip():
                messages.error(request, 'Brand Name is required. Please try again.')
                return redirect('admin_side:brand')

            # Check if the provided Brand_name is unique, excluding the current brand being edited
            if Brand.objects.filter(brand_name=Brand_name).exclude(id=brand_id).exists():
                messages.error(request, 'Brand Name is already taken. Please try again.')
                return redirect('admin_side:add_brand')
            if not re.search(r'[a-zA-Z]', Brand_name):
                    messages.error(request, 'Brand Name must contain both letters and not only numbers. Please try again.')
                    return redirect('admin_side:brand')

            
            if Brand_image:
                if Brand.objects.filter(brand_image=Brand_image).exclude(id=brand_id).exists():
                    messages.error(request, 'Brand Image is already taken. Please try again.')
                    return redirect('admin_side:brand')

            # Update the brand data
            bra.brand_name = Brand_name
            if Brand_image:
                bra.brand_image = Brand_image
            bra.save()

            # Redirect to the brand listing page after successful update
            return redirect('admin_side:brand')
    
        return render(request, 'admin_temp/edit_brand.html')
   else:
        return redirect('admin_login')
    
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

@login_required(login_url='admin_side:admin_login')    
def brand_delete(request, brand_id):
    if request.user.is_superuser:
        brand = get_object_or_404(Brand, id=brand_id)
        
        # Delete the brand
        brand.delete()
        messages.error(request, 'Brand deleted successfully')
        
        return redirect('admin_side:brand')
    else:
        return HttpResponseForbidden("Forbidden")
    



@login_required(login_url='admin_side:admin_login')   
def category(request):
    cat=Category.objects.all()
    context={
        'cat':cat
    }
    
    return render(request,'admin_temp/category.html',context)
@login_required(login_url='admin_side:admin_login')    
def add_category(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            category_name = request.POST.get('category_name')
            cat_image = request.FILES.get('cat_image')
            description = request.POST.get('description')

            # Check if Category Name is empty
            if category_name.strip() == '':
                messages.error(request, 'Category Name is required. Please try again.')
                return redirect('admin_side:category')

            if cat_image is None:
                messages.error(request,'please add photo')
                return redirect('admin_side:category')

            # Check if the provided Category Name is unique
            if Category.objects.filter(category_name=category_name).exists():
                messages.error(request, 'Category Name is already taken. Please try again.')
                return redirect('admin_side:category')

            # Check if the provided Category Image is unique
            if cat_image and Category.objects.filter(cat_image=cat_image).exists():
                messages.error(request, 'Category Image is already taken. Please try again.')
                return redirect('admin_side:category')
            
            if not re.search(r'[a-zA-Z]', category_name):
                    messages.error(request, 'category name Name must contain both letters and not only numbers. Please try again.')
                    return redirect('admin_side:category')

            # Create a new Category object with the correct field name
            category = Category(category_name=category_name, cat_image=cat_image, description=description)
            category.save()

            # Redirect to the brand listing page after successful update
            return redirect('admin_side:category')

        return render(request, 'admin_temp/add_category.html')
    else:
        return redirect('admin_login') 
    
@login_required(login_url='admin_side:admin_login')       
def edit_category(request, cat_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            category_name = request.POST.get('category_name')
            cat_image = request.FILES.get('cat_image')
            description = request.POST.get('description')
            cat = Category.objects.get(id=cat_id)
            if not re.search(r'[a-zA-Z]', category_name):
                    messages.error(request, 'category name Name must contain both letters and not only numbers. Please try again.')
                    return redirect('admin_side:category')
            if not category_name.strip():
                messages.error(request, 'Category Name Is required')
                return redirect('admin_side:category')

            if Category.objects.filter(category_name=category_name).exclude(id=cat_id).exists():
                messages.error(request, 'Category Name Is Already Taken')

            if cat_image:
                if Category.objects.filter(cat_image=cat_image).exclude(id=cat_id).exists():
                    messages.error(request, 'Category image is already taken. Please try again')
                    return redirect('admin_side:category')

            cat.category_name = category_name
            cat.description = description
            if cat_image:
                cat.cat_image = cat_image
            cat.save()
            return redirect('admin_side:category')

        return render(request, 'admin_temp/edit_category.html')
    else:
        return redirect('admin_login') 
    
    
@login_required(login_url='admin_side:admin_login')    
def category_delete(request, cat_id):
    if request.user.is_superuser:
        category = get_object_or_404(Category, id=cat_id)
        
        if not category.is_deleted:
            category.delete()
            messages.error(request, 'Category deleted successfully')
        
        return redirect('admin_side:category')
    else:
        return redirect('admin_login')


@login_required(login_url='admin_side:admin_login')   
def product(request):
    products = Product.objects.all()  # Query the database to get all products
    brand = Brand.objects.all()
    category = Category.objects.all()
    offer = Offer.objects.all()
    

    context = {
        'products': products,  # Pass the products to the template context
        'brand': brand,
        'category': category,
        'offer': offer,
    }
    return render(request, 'admin_temp/product .html', context)

@login_required(login_url='admin_side:admin_login')   
def add_product(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            product_images = request.FILES.getlist('product_image')
            product_name = request.POST.get('product_name')
            product_brand = request.POST.get('product_brand')
            product_offer = request.POST.get('product_offer')
            product_category = request.POST.get('product_category')
            offer_name = request.POST.get('product_offer')
            if offer_name:
                # Offer name provided, check if it exists or create a new one
                offer, created = Offer.objects.get_or_create(offer_name=offer_name)
            else:
                # No offer selected or entered
                offer = None

           
            try:
                product_price = Decimal(request.POST.get('product_price'))
                product_quantity = Decimal(request.POST.get('product_quantity'))
            except InvalidOperation:
                messages.error(request, 'Invalid Attempt. Enter correct values.')
                return redirect('admin_side:product')
                
            if not re.search(r'[a-zA-Z]', product_name):
                messages.error(request, 'Product name must contain both letters and not only numbers. Please try again.')
                return redirect('admin_side:product') 
                
            if not (product_name and product_brand and product_offer and product_category and product_price and product_quantity):
                messages.error(request, 'All fields are required. Please fill them in')
                return redirect('admin_side:product')
            
            if Product.objects.filter(product_name__iexact=product_name).exists():
                messages.error(request, 'A product with this name already exists. Please choose a unique name.')
                return redirect('admin_side:product')
            else:
                brand, created = Brand.objects.get_or_create(brand_name=product_brand)
                category, created = Category.objects.get_or_create(category_name=product_category)
                offer,created=Offer.objects.get_or_create(offer_name=product_offer)
                new_product = Product(
                        product_image=product_images[0],
                        product_name=product_name,
                        product_price=product_price,
                        product_brand=brand,
                        product_offer=offer,
                        product_category=category,
                        product_quantity=product_quantity
                    )

                new_product.save()

                

                for img in product_images:
                        photo = ProductImage.objects.create(product=new_product, image=img)
                        photo.save()

                return redirect('admin_side:product')

    
        brand = Brand.objects.all()
        category = Category.objects.all()
        offer=Offer.objects.all()
        context = {
            'brand': brand,
            'category': category,
            'offer':offer,
        }
        return render(request, 'admin_temp/add_product.html', context)
    else:
        return redirect('admin_login') 
    
    
@login_required(login_url='admin_side:admin_login')    
def edit_product(request, product_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            product_images = request.FILES.getlist('product_images')
            product_name = request.POST.get('product_name')
            product_brand = request.POST.get('product_brand')
            product_offer = request.POST.get('product_offer')
            product_category = request.POST.get('product_category')
            pro = Product.objects.get(id=product_id)

            try:
                product_price = Decimal(request.POST.get('product_price'))
                product_quantity = Decimal(request.POST.get('product_quantity'))
            except InvalidOperation:
                messages.error(request, 'Invalid Attempt. Enter correct values.')
                return redirect('admin_side:product')
            if product_price <= 0 or product_quantity <= 0:
                messages.error(request, 'Product price and quantity must be greater than zero.')
                return redirect('admin_side:product')

            if not re.search(r'[a-zA-Z]', product_name):
                messages.error(request, 'Product name must contain both letters and not only numbers. Please try again.')
                return redirect('admin_side:product')

            # Check for non-empty fields
            if not (product_name and product_brand and product_offer and product_category and product_price and product_quantity):
                messages.error(request, 'All fields are required. Please fill them in.')
                return redirect('admin_side:product')

            # Check for product name uniqueness (case-insensitive) excluding the current product
            if Product.objects.filter(Q(product_name__iexact=product_name) & ~Q(id=product_id)).exists():
                messages.error(request, 'A product with this name already exists. Please choose a unique name.')
                return redirect('admin_side:product')

            brand, created = Brand.objects.get_or_create(brand_name=product_brand)
            category, created = Category.objects.get_or_create(category_name=product_category)
            offer, created = Offer.objects.get_or_create(offer_name=product_offer)

            pro.product_name = product_name
            pro.product_price = product_price
            pro.product_brand = brand
            pro.product_offer = offer
            pro.product_category = category
            pro.product_quantity = product_quantity
            if product_images:
              for img in product_images:
                photo = ProductImage.objects.create(product=pro, image=img)
            photo.save()
            pro.save()

            return redirect('admin_side:product')
        product = Product.objects.all()
        brand = Brand.objects.all()
        category = Category.objects.all()
        offer = Offer.objects.all()
        context = {
            'brand': brand,
            'category': category,
            'offer': offer,
            'product': product
        }
        return render(request, 'admin_temp\edit_product.html', context)
    else:
        return redirect('admin_login')


       
    
@login_required(login_url='admin_side:admin_login')     
def product_delete(request, product_id):
    if request.user.is_superuser:
        product = get_object_or_404(Product, id=product_id)
        if not product.is_deleted:
            product.is_deleted = True
            product.save()
            messages.error(request,'Deleted successfully')
        return redirect('admin_side:product')
    else:
        return redirect('admin_login') 
    
@login_required(login_url='admin_side:admin_login')    
def product_undelete(request, product_id):
    if request.user.is_superuser:
        product = get_object_or_404(Product, id=product_id)
        if product.is_deleted:
            product.is_deleted = False
            product.save()
            messages.error(request,'Un Deleted successfully')
        return redirect('admin_side:product')
    else:
        return redirect('admin_login') 
    
@login_required(login_url='admin_side:admin_login')     
def admin_user(request):
    register_details = User.objects.all()
    context = {
        'register_details': register_details
    }
    return render(request, 'admin_temp/admin_user.html', context)

@login_required(login_url='admin_side:admin_login')    
def user_block(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'User {user.username} is Blocked ')
    return redirect('admin_side:admin_user')

@login_required(login_url='admin_side:admin_login')   
def user_unblock(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'User {user.username} is Unblocked ')
    return redirect('admin_side:admin_user')

    
    
    
@login_required(login_url='admin_side:admin_login')          
def orders(request):
    user_id = request.user.id  # Get the user's ID
    orders = Order.objects.filter(user=user_id)  # Filter orders based on the user's ID
    context={
        'orders':orders
    }

    return render(request,'admin_temp/orders.html',context)

@login_required(login_url='admin_side:admin_login')   
def offer(request):
    off=Offer.objects.all()
    context={
        'off':off
    }
    return render(request,'admin_temp/offer.html',context)


@login_required(login_url='admin_side:admin_login')   
def add_offer(request):
    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        discount_amount = request.POST.get('discount_amount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
       
        # Perform your custom validation here
        if not offer_name or not discount_amount or not start_date or not end_date:
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                discount_amount = int(discount_amount)
                # Perform additional validation if needed
                if discount_amount < 0:
                    messages.error(request, 'Discount amount must be a non-negative integer.')
                else:
                    new_offer = Offer(
                        offer_name=offer_name,
                        discount_amount=discount_amount,
                        start_date=start_date,
                        end_date=end_date,
                    )
                    new_offer.save()
                    messages.success(request, 'Offer added successfully!')
                    return redirect('admin_side:offer')
            except ValueError:
                messages.error(request, 'Discount amount must be a valid integer.')

    return render(request, 'admin_temp/add_offer.html')
   
   
   
@login_required(login_url='admin_side:admin_login')     
def edit_offer(request, offer_id):
    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        discount_amount = request.POST.get('discount_amount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Perform your custom validation here
        if not offer_name or not discount_amount or not start_date or not end_date:
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                discount_amount = int(discount_amount)
                # Perform additional validation if needed
                if discount_amount < 0:
                    messages.error(request, 'Discount amount must be a non-negative integer.')
                else:
                    offer = Offer.objects.get(id=offer_id)
                    offer.offer_name = offer_name
                    offer.discount_amount = discount_amount
                    offer.start_date = start_date
                    offer.end_date = end_date
                    offer.save()
                    messages.success(request, 'Offer updated successfully!')
                    return redirect('admin_side:offer')
            except ValueError:
                messages.error(request, 'Discount amount must be a valid integer.')

    else:
        offer = Offer.objects.get(id=offer_id)
        return render(request, 'admin_temp/edit_offer.html', {'offer': offer})

    return render(request, 'admin_temp/edit_offer.html')


