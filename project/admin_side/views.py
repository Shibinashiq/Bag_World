from decimal import Decimal, InvalidOperation
import re
from django.contrib.auth import authenticate,login
from django.db.models import Q
from django.shortcuts import redirect, render , get_object_or_404
from .models import Brand, ProductImage
from .models import Category
from .models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout


@login_required(login_url='admin_login')  
def admin_dashboard(request):
    return render(request,'admin_temp/dashboard.html')



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

@login_required(login_url='admin_login')
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
        
        
@login_required(login_url='admin_login')       
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
    
    
@login_required(login_url='admin_login') 
def brand_delete(request, brand_id):
    if request.user.is_superuser:
        brand = get_object_or_404( Brand, id=brand_id)
        if not brand.is_deleted:
            brand.is_deleted = True
            brand.save()
            messages.error(request,'Deleted successfully')
        return redirect('admin_side:brand')
    else:
        return redirect('admin_login')
    
@login_required(login_url='admin_login')    
def brand_undelete(request, brand_id):
    if request.user.is_superuser:
        brand = get_object_or_404( Brand, id=brand_id)
        if brand.is_deleted:
            brand.is_deleted = False
            brand.save()
            messages.error(request,'Un Deleted successfully')
        return redirect('admin_side:brand')
    else:
        return redirect('admin_login')
    




def category(request):
    cat=Category.objects.all()
    context={
        'cat':cat
    }
    
    return render(request,'admin_temp/category.html',context)
@login_required(login_url='admin_login')   
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
    
@login_required(login_url='admin_login')     
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
    
@login_required(login_url='admin_login')   
def category_delete(request, cat_id):
    if request.user.is_superuser:
        category = get_object_or_404(Category, id=cat_id)
        if not category.is_deleted:
            category.is_deleted = True
            category.save()
            messages.error(request,'Deleted successfully')
        return redirect('admin_side:category')
    else:
        return redirect('admin_login') 
    
    
@login_required(login_url='admin_login')      
def category_undelete(request, cat_id):
    if request.user.is_superuser:
        category = get_object_or_404(Category, id=cat_id)
        if category.is_deleted:
            category.is_deleted = False
            category.save()
            messages.error(request,'Un Deleted successfully')
        return redirect('admin_side:category')
    else:
        return redirect('admin_login') 



@login_required(login_url='admin_login')  
def product(request):
    product=Product.objects.all()
    brand=Brand.objects.all()
    category=Category.objects.all()
    context={
        'product':product,
        'brand' :brand,
        'category':category,
    }
    return render(request, 'admin_temp\product .html',context)

@login_required(login_url='admin_login')  
def add_product(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            product_images = request.FILES.getlist('product_image')
            product_name = request.POST.get('product_name')
            product_brand = request.POST.get('product_brand')
            product_offer = request.POST.get('product_offer')
            product_category = request.POST.get('product_category')
            print('the product image is the', product_images)
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

                new_product = Product(
                        product_image=product_images[0],
                        product_name=product_name,
                        product_price=product_price,
                        product_brand=brand,
                        product_offer=product_offer,
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
        context = {
            'brand': brand,
            'category': category,
        }
        return render(request, 'admin_temp/add_product.html', context)
    else:
        return redirect('admin_login') 
    
@login_required(login_url='admin_login')   
def edit_product(request,product_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            product_image = request.FILES.get('product_image')
            product_name = request.POST.get('product_name')
            product_brand = request.POST.get('product_brand')
            product_offer = request.POST.get('product_offer')
            product_category = request.POST.get('product_category')
            pro=Product.objects.get(id=product_id)

            try:
                product_price = Decimal(request.POST.get('product_price'))
                product_quantity = Decimal(request.POST.get('product_quantity'))
            except InvalidOperation:
                messages.error(request, 'Invalid Attempt. Enter correct values.')
                return redirect('admin_side:product')
            if product_price or product_quantity <= 0:
                messages.error(request, 'Product price must be greater than zero.')
                return redirect('admin_side:product')
            
            if not re.search(r'[a-zA-Z]', product_name):
                    messages.error(request, 'product name Name must contain both letters and not only numbers. Please try again.')
                    return redirect('admin_side:product') 

            # Check for non-empty fields
            if not (product_image and product_name and product_brand and product_offer and product_category and product_price and product_quantity):
                messages.error(request, 'All fields are required. Please fill them in.')
                return redirect('admin_side:product')

            # Check for product name uniqueness (case-insensitive) excluding the current product
            if Product.objects.filter(Q(product_name__iexact=product_name) & ~Q(id=product_id)).exists():
                messages.error(request, 'A product with this name already exists. Please choose a unique name.')
                return redirect('admin_side:product')
            
            brand,created=Brand.objects.get_or_create(brand_name=product_brand)
            category,created=Category.objects.get_or_create(category_name=product_category)
                    
            pro.product_name=product_name
            pro.product_price=product_price
            pro.product_brand=product_brand
            pro.product_offer=product_offer
            pro.product_category=product_category
            pro.product_quantity=product_quantity
            if product_image:
                pro.product_image=product_image
            pro.save()
        
            return redirect('admin_side:product')
        
        brand = Brand.objects.all()
        category = Category.objects.all()
        context = {
            'brand': brand,
            'category': category,
        }
        return render(request,'admin_temp\edit_product.html',context)
    else:
        return redirect('admin_login') 
@login_required(login_url='admin_login')   
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
    
@login_required(login_url='admin_login')   
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
    
def admin_user(request):
    register_details = User.objects.all()
    context = {
        'register_details': register_details
    }
    return render(request, 'admin_temp/admin_user.html', context)


def user_block(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'User {user.username} is Blocked ')
    return redirect('admin_side:admin_user')

def user_unblock(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'User {user.username} is Unblocked ')
    return redirect('admin_side:admin_user')

    
    