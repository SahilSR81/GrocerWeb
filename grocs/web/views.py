from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from superadmin.models import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
import random
from django.views.decorators.csrf import csrf_exempt

from superadmin.models import Cart, Order, OrderItem, Product, Fruit
from .models import Customer

# Create your views here.

from superadmin.models import Category

def home(request):
    # Title and name
    title = 'Grocer'
    name = 'Deepak'
    
    # Fetch the first 4 categories and their associated products
    cat_list = Category.objects.prefetch_related('product_set').all()[:4]
    
    # Render the homepage template with the categories
    return render(request, 'web_html/index.html', {'title': title, 'name': name, 'cat': cat_list})

def contact(request):
    # return HttpResponse('Hello')
    title = 'contact'
    return render(request,'web_html/contact.html',{'title':title,})

def loginwithgamil(request):
    # return HttpResponse('Hello')
    title = 'loginwithgmail'
    return render(request,'web_html/loginwithgmail.html',{'title':title,})






def login(request):
    title = 'Login Page'
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Both fields are required')
            return redirect('login')

        user = Customer.objects.filter(email=email, password=password).first()

        if user:
            request.session['cust_id'] = user.id
            request.session['cust_first'] = user.first
            messages.success(request, 'Login successful')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'web_html/lo.html', {'title': title})


def cleaning(request):
    # return HttpResponse('Hello')
    title = 'cleaning'
    return render(request,'web_html/cleaning.html',{'title':title,})

def table(request):
    title = 'Data'
    custdata = Customer.objects.filter(status = 1)
    return render(request,'web_html/table.html',{'title':title,'Data':custdata})


def edit_cust(request,id):
    title = 'Edit Customerdata'
    cust = Customer.objects.get(id=id)
    if request.method == 'POST':
        first = request.POST['first']
        last = request.POST['last']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        image = request.FILES['image']
        # address = request.POST['address']
        gender = request.POST['gender']
        cust.first = first
        cust.last = last
        cust.email = email
        cust.mobile = phone
        cust.password = password
        cust.image = image
        # cust.address = address
        cust.gender = gender
        cust.save()
        messages.info(request,'Update Successful')
        return redirect('table')
    return render(request,'web_html/edit_cust.html',{'title':title,'data':cust,'id':id})


def del_cust(request,id):
    title = 'Delete CustomerData'
    cust = Customer.objects.get(id=id)
    if request.method == 'POST':
        cust.delete()
        messages.info(request,'Delete Successful')
        return redirect('table')

    return render(request,'web_html/del_cust.html',{'title':title,'data':'cust','id':id})

def profile(request):
    title = 'Profile'
    cust_id = request.session['cust_id']
    cust = Customer.objects.get(id=cust_id)
    if request.method == 'POST':
        first = request.POST['first']
        last = request.POST['last']
        email = request.POST['email']
        mobile = request.POST['mobile']
        image = request.FILES['image']
        gender = request.POST['gender']
        cust.first = first
        cust.last = last
        cust.email = email
        cust.mobile = mobile
        cust.image = image
        cust.gender = gender
        cust.save()
        return redirect('profile')
    return render(request,'web_html/profile.html',{'title':title,'cust':cust})

# def logout(request):
#     del request.session['cust_id']
#     del request.session['cust_first']
#     messages.info(request,'Logout success')
#     return redirect('home')

def logout(request):
    request.session.pop('cust_first', None)
    request.session.pop('cust_id', None)
    return redirect('login')




def cart_list(request):
    title = 'Cart List'
    cust_id = request.session.get('cust_id')
    if cust_id:
        cart_data = Cart.objects.filter(customer_id=cust_id, status=1)

        total_original_price = 0
        total_cart_amount = 0

        for item in cart_data:
            if item.product:
                total_original_price += item.product.pprice * item.quantity
                total_cart_amount += item.product.psellprice * item.quantity
            elif item.fruit:
                total_original_price += item.fruit.fprice * item.quantity
                total_cart_amount += item.fruit.fsellprice * item.quantity

        total_discount = total_original_price - total_cart_amount
        tax_percentage = 10
        tax_amount = total_cart_amount * (tax_percentage / 100)
        final_total = total_cart_amount + tax_amount

        return render(request, 'web_html/cart.html', {
            'title': title,
            'cart_data': cart_data,
            'total_cart_amount': round(total_cart_amount, 2),
            'total_original_price': round(total_original_price, 2),
            'total_discount': round(total_discount, 2),
            'tax_amount': round(tax_amount, 2),
            'final_total': round(final_total, 2)
        })
    return redirect('login')
# 
# def add_to_cart(request, id, item_type):
#     title = 'Cart Details'
#     cust_id = request.session.get('cust_id')

#     if not cust_id:
#         return redirect('login')

#     if item_type == 'fruit':
#         try:
#             prod = Fruit.objects.get(id=id)
#             existing_cart_item = Cart.objects.filter(customer_id=cust_id, fruit_id=id, status=1).first()

#             if existing_cart_item:
#                 # If item already in the cart, increase quantity
#                 existing_cart_item.quantity += 1
#                 existing_cart_item.total_amt = existing_cart_item.quantity * prod.fprice
#                 existing_cart_item.save()
#             else:
#                 # Add new fruit to the cart
#                 Cart.objects.create(
#                     customer_id=cust_id,
#                     fruit_id=id,
#                     quantity=1,
#                     total_amt=prod.fprice
#                 )
#         except Fruit.DoesNotExist:
#             messages.error(request, 'Fruit not found')
#             return redirect('shop')

#     elif item_type == 'product':
#         try:
#             prod = Product.objects.get(id=id)
#             existing_cart_item = Cart.objects.filter(customer_id=cust_id, product_id=id, status=1).first()

#             if existing_cart_item:
#                 # If product exists, increase quantity
#                 existing_cart_item.quantity += 1
#                 existing_cart_item.total_amt = existing_cart_item.quantity * prod.psellprice
#                 existing_cart_item.save()
#             else:
#                 # Create new cart item for product
#                 Cart.objects.create(
#                     customer_id=cust_id,
#                     product_id=id,
#                     quantity=1,
#                     total_amt=prod.psellprice
#                 )
#         except Product.DoesNotExist:
#             messages.error(request, 'Product not found')
#             return redirect('shop')

#     # Fetch updated cart data
#     cart_data = Cart.objects.filter(customer_id=cust_id, status=1)
#     total_item = len(cart_data)

#     return render(request, 'web_html/cart.html', {'title': title, 'cart_data': cart_data, 'total_item': total_item})



def add_to_cart(request, id, item_type):
    title = 'Cart Details'
    cust_id = request.session.get('cust_id')

    if not cust_id:
        return redirect('login')

    if item_type == 'fruit':
        try:
            prod = Fruit.objects.get(id=id)
            existing_cart_item = Cart.objects.filter(customer_id=cust_id, fruit_id=id, status=1).first()

            if existing_cart_item:
                existing_cart_item.quantity += 1
                existing_cart_item.total_amt = existing_cart_item.quantity * prod.fsellprice
                existing_cart_item.save()
            else:
                Cart.objects.create(
                    customer_id=cust_id,
                    fruit_id=id,
                    quantity=1,
                    total_amt=prod.fsellprice
                )
        except Fruit.DoesNotExist:
            messages.error(request, 'Fruit not found')
            return redirect('shop')

    elif item_type == 'product':
        try:
            prod = Product.objects.get(id=id)
            existing_cart_item = Cart.objects.filter(customer_id=cust_id, product_id=id, status=1).first()

            if existing_cart_item:
                existing_cart_item.quantity += 1
                existing_cart_item.total_amt = existing_cart_item.quantity * prod.psellprice
                existing_cart_item.save()
            else:
                Cart.objects.create(
                    customer_id=cust_id,
                    product_id=id,
                    quantity=1,
                    total_amt=prod.psellprice
                )
        except Product.DoesNotExist:
            messages.error(request, 'Product not found')
            return redirect('shop')

    # Recalculate cart summary
    cart_data = Cart.objects.filter(customer_id=cust_id, status=1)

    total_original_price = 0
    total_cart_amount = 0

    for item in cart_data:
        if item.product:
            total_original_price += item.product.pprice * item.quantity
            total_cart_amount += item.product.psellprice * item.quantity
        elif item.fruit:
            total_original_price += item.fruit.fprice * item.quantity
            total_cart_amount += item.fruit.fsellprice * item.quantity

    total_discount = total_original_price - total_cart_amount
    tax_percentage = 10
    tax_amount = total_cart_amount * (tax_percentage / 100)
    final_total = total_cart_amount + tax_amount

    return render(request, 'web_html/cart.html', {
        'title': title,
        'cart_data': cart_data,
        'total_cart_amount': round(total_cart_amount, 2),
        'total_original_price': round(total_original_price, 2),
        'total_discount': round(total_discount, 2),
        'tax_amount': round(tax_amount, 2),
        'final_total': round(final_total, 2)
    })
def remove_product(request, id):
    cust_id = request.session.get('cust_id')
    if not cust_id:
        return redirect('login')
    
    try:
        # Now using Cart's ID
        cart_item = Cart.objects.filter(
            id=id,
            customer_id=cust_id,
            status=1
        ).first()
        
        if cart_item:
            cart_item.delete()
            messages.success(request, 'Item removed from cart successfully')
        else:
            messages.error(request, 'Item not found in cart')
    except Exception as e:
        messages.error(request, 'An error occurred: ' + str(e))
    
    return redirect('cart_list')






def update_cart_quantity(request, id):
    if 'cust_id' not in request.session:
        return redirect('login')
    
    cust_id = request.session['cust_id']
    
    if request.method == 'POST':
        cart_item = Cart.objects.filter(id=id, customer_id=cust_id, status=1).first()

        if cart_item:
            action = request.POST.get('action')
            
            if action == 'plus':
                cart_item.quantity += 1
            elif action == 'minus' and cart_item.quantity > 1:
                cart_item.quantity -= 1
            
            if cart_item.product:
                cart_item.total_amt = cart_item.quantity * cart_item.product.psellprice
            elif cart_item.fruit:
                cart_item.total_amt = cart_item.quantity * cart_item.fruit.fprice
            
            cart_item.save()
            messages.success(request, 'Cart updated successfully')
        else:
            messages.error(request, 'Item not found in cart')
    
    return redirect('cart_list')

def shop(request):
    title = 'Shop'
    fruit_list = Menus.objects.prefetch_related('fruit_set').all()[0:4]
    return render(request,'web_html/shop.html',{'title':title,'cat':fruit_list})




def deliveryone(request):
    # return HttpResponse('Hello')
    title = 'delivery'
    return render(request,'web_html/deliveryone.html',{'title':title,})

def payment(request):
    # return HttpResponse('Hello')
    title = 'delivery'
    return render(request,'web_html/payment.html',{'title':title,})


def about(request):
    # return HttpResponse('Hello')
    title = 'about'
    return render(request,'web_html/about.html',{'title':title,})

# def add_to_cart(request, id, item_type):
#     title = 'Cart Details'
#     cust_id = request.session.get('cust_id')

#     if not cust_id:
#         return redirect('login')

#     if item_type == 'fruit':
#         try:
#             prod = Fruit.objects.get(id=id)
#             existing_cart_item = Cart.objects.filter(customer_id=cust_id, fruit_id=id, status=1).first()

#             if existing_cart_item:
#                 # If item already in the cart, increase quantity
#                 existing_cart_item.quantity += 1
#                 existing_cart_item.total_amt = existing_cart_item.quantity * prod.fprice
#                 existing_cart_item.save()
#             else:
#                 # Add new fruit to the cart
#                 Cart.objects.create(
#                     customer_id=cust_id,
#                     fruit_id=id,
#                     quantity=1,
#                     total_amt=prod.fprice
#                 )
#         except Fruit.DoesNotExist:
#             messages.error(request, 'Fruit not found')
#             return redirect('shop')

#     elif item_type == 'product':
#         try:
#             prod = Product.objects.get(id=id)
#             existing_cart_item = Cart.objects.filter(customer_id=cust_id, product_id=id, status=1).first()

#             if existing_cart_item:
#                 # If product exists, increase quantity
#                 existing_cart_item.quantity += 1
#                 existing_cart_item.total_amt = existing_cart_item.quantity * prod.psellprice
#                 existing_cart_item.save()
#             else:
#                 # Create new cart item for product
#                 Cart.objects.create(
#                     customer_id=cust_id,
#                     product_id=id,
#                     quantity=1,
#                     total_amt=prod.psellprice
#                 )
#         except Product.DoesNotExist:
#             messages.error(request, 'Product not found')
#             return redirect('shop')

#     # Fetch updated cart data
#     cart_data = Cart.objects.filter(customer_id=cust_id, status=1)
#     total_item = len(cart_data)

#     return render(request, 'web_html/cart.html', {'title': title, 'cart_data': cart_data, 'total_item': total_item})

def remove_product(request, id):
    cust_id = request.session.get('cust_id')
    if not cust_id:
        return redirect('login')
    
    try:
        # Now using Cart's ID
        cart_item = Cart.objects.filter(
            id=id,
            customer_id=cust_id,
            status=1
        ).first()
        
        if cart_item:
            cart_item.delete()
            messages.success(request, 'Item removed from cart successfully')
        else:
            messages.error(request, 'Item not found in cart')
    except Exception as e:
        messages.error(request, 'An error occurred: ' + str(e))
    
    return redirect('cart_list')






def update_cart_quantity(request, id):
    if 'cust_id' not in request.session:
        return redirect('login')
    
    cust_id = request.session['cust_id']
    
    if request.method == 'POST':
        cart_item = Cart.objects.filter(id=id, customer_id=cust_id, status=1).first()

        if cart_item:
            action = request.POST.get('action')
            
            if action == 'plus':
                cart_item.quantity += 1
            elif action == 'minus' and cart_item.quantity > 1:
                cart_item.quantity -= 1
            
            if cart_item.product:
                cart_item.total_amt = cart_item.quantity * cart_item.product.psellprice
            elif cart_item.fruit:
                cart_item.total_amt = cart_item.quantity * cart_item.fruit.fprice
            
            cart_item.save()
            messages.success(request, 'Cart updated successfully')
        else:
            messages.error(request, 'Item not found in cart')
    
    return redirect('cart_list')

def shop(request):
    title = 'Shop'
    fruit_list = Menus.objects.prefetch_related('fruit_set').all()[0:4]
    return render(request,'web_html/shop.html',{'title':title,'cat':fruit_list})




def deliveryone(request):
    # return HttpResponse('Hello')
    title = 'delivery'
    return render(request,'web_html/deliveryone.html',{'title':title,})

def payment(request):
    # return HttpResponse('Hello')
    title = 'delivery'
    return render(request,'web_html/payment.html',{'title':title,})


def about(request):
    # return HttpResponse('Hello')
    title = 'about'
    return render(request,'web_html/about.html',{'title':title,})

def add_to_wishlist(request, id):
    if 'cust_id' not in request.session:
        messages.info(request, 'Please login to add to wishlist')
        return redirect('login')

    try:
        cust_id = request.session['cust_id']
        product_type = request.GET.get('type')  # 'product' or 'fruit'

        # Validate product type and fetch the item
        if product_type == 'fruit':
            prod = Fruit.objects.get(id=id)
            existing_wishlist_item = Cart.objects.filter(customer_id=cust_id, fruit_id=id, is_wishlist=True).first()
            price = prod.fprice
            product_id = None
            fruit_id = id
        elif product_type == 'product':
            prod = Product.objects.get(id=id)
            existing_wishlist_item = Cart.objects.filter(customer_id=cust_id, product_id=id, is_wishlist=True).first()
            price = prod.psellprice
            product_id = id
            fruit_id = None
        else:
            messages.error(request, 'Invalid product type')
            return redirect('home')

        if existing_wishlist_item:
            messages.info(request, 'Product already in wishlist')
        else:
            Cart.objects.create(
                customer_id=cust_id,
                product_id=product_id,
                fruit_id=fruit_id,
                quantity=1,
                total_amt=price,
                is_wishlist=True
            )
            messages.success(request, 'Product added to wishlist')

        return redirect('wishlist')

    except (Product.DoesNotExist, Fruit.DoesNotExist):
        messages.error(request, 'Product not found')
        return redirect('home')
# def wishlist(request):
#     if 'cust_id' not in request.session:
#         messages.info(request, 'Please login to view wishlist')
#         return redirect('login')

#     title = 'Wishlist'
#     cust_id = request.session['cust_id']

#     wishlist_items = Cart.objects.filter(customer_id=cust_id, is_wishlist=True, status=1).select_related('product', 'fruit')

#     return render(request, 'web_html/wishlist.html', {
#         'title': title,
#         'wishlist_items': wishlist_items
#     })

def remove_from_wishlist(request, id):
    if 'cust_id' not in request.session:
        messages.info(request, 'Please login to remove from wishlist')
        return redirect('login')

    cust_id = request.session['cust_id']

    try:
        product_type = request.GET.get('type')
        
        if product_type == 'fruit':
            wishlist_item = Cart.objects.get(customer_id=cust_id, fruit_id=id, is_wishlist=True)
        else:
            wishlist_item = Cart.objects.get(customer_id=cust_id, product_id=id, is_wishlist=True)

        wishlist_item.delete()
        messages.success(request, 'Product removed from wishlist')
    except Cart.DoesNotExist:
        messages.error(request, 'Product not found in wishlist')

    return redirect('wishlist')

def move_to_cart(request, id):
    if 'cust_id' not in request.session:
        messages.info(request, 'Please login')
        return redirect('login')

    cust_id = request.session['cust_id']

    try:
        product_type = request.GET.get('type')  # 'type' param to distinguish product/fruit
        
        if product_type == 'fruit':
            wishlist_item = Cart.objects.get(customer_id=cust_id, fruit_id=id, is_wishlist=True)
            unit_price = wishlist_item.fruit.fprice
        else:
            wishlist_item = Cart.objects.get(customer_id=cust_id, product_id=id, is_wishlist=True)
            unit_price = wishlist_item.product.psellprice

        # Check if item already exists in the cart
        existing_cart_item = Cart.objects.filter(
            customer_id=cust_id,
            product_id=id if product_type != 'product' else None,
            fruit_id=id if product_type == 'fruit' else None,
            is_wishlist=False
        ).first()

        if existing_cart_item:
            # Increase quantity if it exists in the cart
            existing_cart_item.quantity += 1
            existing_cart_item.total_amt = existing_cart_item.quantity * unit_price
            existing_cart_item.save()
        else:
            # Create new cart item
            Cart.objects.create(
                customer_id=cust_id,
                product_id=id if product_type != 'fruit' else None,
                fruit_id=id if product_type == 'fruit' else None,
                quantity=1,
                total_amt=unit_price,
                is_wishlist=False
            )

        # Remove from wishlist
        wishlist_item.delete()

        messages.success(request, 'Product moved to cart')
        return redirect('cart_list')

    except Cart.DoesNotExist:
        messages.error(request, 'Product not found in wishlist')
        return redirect('wishlist')
    
    
def wishlist(request):
    if 'cust_id' not in request.session:
     return redirect('login')

    cust_id = request.session['cust_id']
    wishlist_items = Cart.objects.filter(customer_id=cust_id, is_wishlist=True)

    return render(request, 'web_html/wishlist.html', {'wishlist_items': wishlist_items})
# def wishlist(request):
#     if 'cust_id' not in request.session:
#         messages.info(request, 'Please login to view wishlist')
#         return redirect('login')

#     title = 'Wishlist'
#     cust_id = request.session['cust_id']

#     wishlist_items = Cart.objects.filter(customer_id=cust_id, is_wishlist=True, status=1).select_related('product', 'fruit')

#     return render(request, 'web_html/wishlist.html', {
#         'title': title,
#         'wishlist_items': wishlist_items
#     })

# def remove_from_wishlist(request, id):
#     if 'cust_id' not in request.session:
#         messages.info(request, 'Please login to remove from wishlist')
#         return redirect('login')

#     cust_id = request.session['cust_id']

#     try:
#         product_type = request.GET.get('type')
        
#         if product_type == 'fruit':
#             wishlist_item = Cart.objects.get(customer_id=cust_id, fruit_id=id, is_wishlist=True)
#         else:
#             wishlist_item = Cart.objects.get(customer_id=cust_id, product_id=id, is_wishlist=True)

#         wishlist_item.delete()
#         messages.success(request, 'Product removed from wishlist')
#     except Cart.DoesNotExist:
#         messages.error(request, 'Product not found in wishlist')

#     return redirect('wishlist')

# def move_to_cart(request, id):
#     if 'cust_id' not in request.session:
#         messages.info(request, 'Please login')
#         return redirect('login')

#     cust_id = request.session['cust_id']

#     try:
#         product_type = request.GET.get('type')  # 'type' param to distinguish product/fruit
        
#         if product_type == 'fruit':
#             wishlist_item = Cart.objects.get(customer_id=cust_id, fruit_id=id, is_wishlist=True)
#         else:
#             wishlist_item = Cart.objects.get(customer_id=cust_id, product_id=id, is_wishlist=True)

#         # Check if item already exists in the cart
#         existing_cart_item = Cart.objects.filter(customer_id=cust_id, product_id=id if not product_type else None,
#                                                  fruit_id=id if product_type == 'fruit' else None, is_wishlist=False).first()

#         if existing_cart_item:
#             # Increase quantity if it exists in the cart
#             existing_cart_item.quantity += 1
#             existing_cart_item.total_amt = existing_cart_item.quantity * (existing_cart_item.product.psellprice if not product_type else existing_cart_item.fruit.fprice)
#             existing_cart_item.save()
#         else:
#             # Create new cart item
#             Cart.objects.create(
#                 customer_id=cust_id,
#                 product_id=id if not product_type else None,
#                 fruit_id=id if product_type == 'fruit' else None,
#                 quantity=1,
#                 total_amt=wishlist_item.product.psellprice if not product_type else wishlist_item.fruit.fprice,
#                 is_wishlist=False
#             )

#         # Remove from wishlist
#         wishlist_item.delete()

#         messages.success(request, 'Product moved to cart')
#         return redirect('cart_list')

#     except Cart.DoesNotExist:
#         messages.error(request, 'Product not found in wishlist')
#         return redirect('wishlist')
    



   


def list(request):
    messages = Message.objects.all().order_by('-created_at')
    return render(request, 'list.html', {'messages': messages})





from django.shortcuts import render, redirect
from .models import ContactMessage
from django.contrib import messages

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, "Your message has been submitted!")
        return redirect('contact')
    
    return render(request, "web_html/contact.html")





def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            messages.error(request, "Please provide a valid email address.")
            return redirect('send_otp')

        otp = str(random.randint(100000, 999999))
        print("Generated OTP:", otp)  # DEBUG

        # Save or update OTP
        OTPVerification.objects.update_or_create(email=email, defaults={'otp': otp})

        # Compose email
        subject = 'Your Grocer OTP Code'
        message = f"""
Hi,

You requested to log in or verify your identity at Grocer.

🔐 Your One-Time Password (OTP) is: {otp}

This OTP is valid for 10 minutes. If you did not request this, please ignore this email.

Thank you,  
Team Grocer
"""
        send_mail(
            subject,
            message,
            'yourprojectemail@example.com',
            [email],
            fail_silently=False,
        )

        # Save email to session
        request.session['email'] = email
        print("Saved email in session:", email)  # DEBUG

        messages.success(request, f"An OTP has been sent to {email}")
        return redirect('verify_otp')

    return render(request, 'web_html/send_otp.html')



from django.contrib import messages
from .models import OTPVerification, Customer

def verify_otp(request):
    if request.method == 'POST':
        email = request.session.get('email')
        entered_otp = request.POST['otp']
        print("Verifying OTP for:", email)  # DEBUG

        try:
            otp_obj = OTPVerification.objects.get(email=email)
            print("Correct OTP:", otp_obj.otp)  # DEBUG

            if otp_obj.otp == entered_otp:
                try:
                    customer = Customer.objects.get(email=email)
                    request.session['cust_id'] = customer.id
                    request.session['cust_first'] = customer.first  # add this
                    messages.success(request, 'Logged in successfully!')
                    return redirect('profile')  # Change to account page if needed
                except Customer.DoesNotExist:
                    messages.info(request, "No account. Please register.")
                    return redirect('registration')
            else:
                messages.error(request, 'Incorrect OTP')
        except OTPVerification.DoesNotExist:
            messages.error(request, 'OTP not found. Please try again.')

    return render(request, 'web_html/verify_otp.html')
    




def registration(request):
    title = 'Registration page'
    if request.method=="POST":
        first = request.POST['first']
        last = request.POST['last']
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['mobile']
        image = request.FILES['image']
        gender = request.POST['gender']
        cust = Customer.objects.filter(email=email).first()
        if cust is None:
            Customer.objects.create(first = first,last = last, mobile = mobile , email=email,password = password,image=image,gender = gender)
            # subject = 'register'
            # message =  'register otp' + str(random.randint(0000,9999))
            # from_user = settings.EMAIL_HOST_USER
            # send_mail(subject,message,from_user,[email])
        else:
            # return HttpResponse("Email id already exists")
            messages.info(request,"Email id already exists")
            return redirect('registration')
        messages.info(request,"Registered success")
        return redirect('login')
               
    return render(request,'web_html/register.html',{'title':title})



# for order

@csrf_exempt
def deliveryone(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')

    customer = Customer.objects.get(id=customer_id)
    cart_items = Cart.objects.filter(customer=customer, status=True, is_wishlist=False)

    if request.method == 'POST':
        address = request.POST.get('address')
        if not address:
            messages.error(request, 'Please provide a delivery address.')
            return redirect('deliveryone')

        # Create Order
        order = Order.objects.create(customer=customer, address=address)

        # Add items to order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product if item.product else None,
                fruit=item.fruit if item.fruit else None,
                quantity=item.quantity,
                price=item.total_amt
            )
        # Clear cart
        cart_items.delete()

        # Send email to customer
        subject = 'Order Confirmation - Grocer'
        message = f"Hi {customer.name},\n\nYour order has been placed successfully!\nOrder ID: {order.id}\nDelivery Address: {address}\n\nThanks for shopping with us!"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [customer.email])

        messages.success(request, 'Order placed successfully. Confirmation sent to your email.')
        return redirect('home')

    return render(request, 'web/delivery_form.html', {'cart_items': cart_items})


def my_orders(request):
    customer_id = request.session.get('customer_id')
    
    # Check if customer_id exists in session
    if not customer_id:
        return redirect('login')
    
    # Retrieve customer object or return 404 if not found
    customer = get_object_or_404(Customer, id=customer_id)
    
    # Retrieve orders related to the customer, ordered by creation date
    orders = Order.objects.filter(customer=customer).order_by('-created_at')

    # Check if there are no orders
    if not orders:
        message = "You have no orders yet."
    else:
        message = None

    # Pass orders and message to the template
    return render(request, 'web/my_orders.html', {'orders': orders, 'message': message})


# from datetime import datetime

def place_order(request):
    if request.method == "POST":
        cust_id = request.session.get('cust_id')
        if not cust_id:
            messages.error(request, "You must be logged in to place an order.")
            return redirect('login')

        customer = Customer.objects.get(id=cust_id)

        address = CustomerAddress.objects.filter(customer=customer).last()
        if not address:
            messages.error(request, "No address found. Please add an address first.")
            return redirect('save_address')

        cart_items = Cart.objects.filter(customer_id=cust_id, status=1)
        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('cart_list')

        total_amount = sum(item.total_amt for item in cart_items)

        order = Order.objects.create(
    customer=customer,
    address=f"{address.house_no}, {address.area}, {address.city}, {address.pincode}, {address.state} ({address.address_type})",
    city=address.city,  # ✅ Save city separately here
    total_amount=total_amount,
    status='Pending'
)

        for item in cart_items:
            if item.product:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.psellprice
                )
            elif item.fruit:
                OrderItem.objects.create(
                    order=order,
                    fruit=item.fruit,
                    quantity=item.quantity,
                    price=item.fruit.fprice
                )

        cart_items.update(status=0)
        messages.success(request, "Your order has been placed successfully.")
        return redirect('order_success')

    return redirect('order_success')

def save_address(request):
    if request.method == "POST":
        cust_id = request.session.get('cust_id')
        if not cust_id:
            messages.error(request, "You must be logged in to place an order.")
            return redirect('login')

        customer = Customer.objects.get(id=cust_id)

        house_no = request.POST.get('house_no')
        area = request.POST.get('area')
        city = request.POST.get('city')  # ✅ NEW LINE
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        address_type = request.POST.get('address_type')
        extra_notes = request.POST.get('address')  # optional notes

        CustomerAddress.objects.create(
            customer=customer,
            house_no=house_no,
            area=area,
            city=city,  # ✅ NEW LINE
            pincode=pincode,
            state=state,
            address_type=address_type,
            extra_notes=extra_notes
        )

        messages.success(request, "Address saved successfully.")
        return redirect('place_order')

    return render(request, 'web_html/save_address.html')

from django.shortcuts import render

def order_success(request):
    return render(request, 'order_success.html')

from django.shortcuts import get_object_or_404

def order_history(request):
    if 'cust_id' not in request.session:
        return redirect('login')

    customer_id = request.session['cust_id']
    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer=customer).order_by('-id')
    
    # Ensure orders contain the city field
    for order in orders:
        print(order.city)  # Debug: print city field for each order
    
    return render(request, 'web_html/order_history.html', {'orders': orders})
def track_order(request, order_id):
    # Get customer id from session
    customer_id = request.session.get('cust_id')
    if not customer_id:
        return redirect('login')

    # Fetch the customer and order details
    customer = get_object_or_404(Customer, id=customer_id)
    order = get_object_or_404(Order, id=order_id, customer=customer)

    # Render the order details page
    return render(request, 'web_html/track_order.html', {'order': order})

def cancel_order(request, order_id):
    # Get customer id from session
    customer_id = request.session.get('cust_id')
    if not customer_id:
        return redirect('login')

    # Fetch the customer and order
    customer = get_object_or_404(Customer, id=customer_id)
    order = get_object_or_404(Order, id=order_id, customer=customer)

    # Only allow cancellation of orders with status "Pending"
    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f'Order #{order.id} has been cancelled successfully.')
    else:
        messages.error(request, f'Order #{order.id} cannot be cancelled as it is already {order.status}.')

    return redirect('order_history')

from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import EmailMessage

def generate_invoice_pdf(order):
    template = get_template('invoice_template.html')  # You need to create this template
    html = template.render({'order': order})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None

from django.shortcuts import render
from superadmin.models import Product, Fruit

def search_products(request):
    query = request.GET.get('query', '').strip()
    products = Product.objects.filter(pname__icontains=query)
    fruits = Fruit.objects.filter(fname__icontains=query)

    context = {
        'query': query,
        'products': products,
        'fruits': fruits,
    }
    return render(request, 'web_html/search_results.html', context)

from django.core.mail import EmailMessage
from django.conf import settings

def send_invoice_email(order):
    pdf = generate_invoice_pdf(order)
    if pdf:
        subject = f"Invoice for Your Order #{order.id} - Grocer"
        message = f"Hi {order.customer.first} {order.customer.last},\n\nPlease find attached the invoice for your recent order."
        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.customer.email],  # Make sure your Customer model has `email`
        )
        email.attach(f"Invoice_{order.id}.pdf", pdf, 'application/pdf')
        email.send()


def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    pdf = generate_invoice_pdf(order)
    send_invoice_email(order)  # Sends to customer's email
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{order.id}.pdf"'
    return response
def generate_invoice_pdf(order):
    template = get_template('web_html/invoice_template.html')
    context = {'order': order}
    html = template.render(context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return result.getvalue()
    return None


# from superadmin.models import Category, Product

def category_products(request, cat_id):
    category = Category.objects.get(id=cat_id)
    products = Product.objects.filter(category=category)
    return render(request, 'web_html/category_products.html', {'category': category, 'products': products})

# web/views.py
# from django.shortcuts import render, redirect
# from .models import Customer
# from django.contrib import messages

# def customer_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             customer = Customer.objects.get(email=email, password=password)
#             request.session['customer_id'] = customer.id  # ✅ required
#             return redirect('home')  # or any logged-in page
#         except Customer.DoesNotExist:
#             messages.error(request, 'Invalid email or password')
#             return redirect('order_success')
#     return render(request, 'order_success')



# def update_cart_quantity(request, id):
#     cust_id = request.session.get('cust_id')
#     if not cust_id:
#         return redirect('login')
    
#     if request.method == 'POST':
#         try:
#             cart_item = Cart.objects.get(customer_id=cust_id, product_id=id, status=1)
            
#             # Get the action and current quantity
#             action = request.POST.get('action')
            
#             if action == 'plus':
#                 cart_item.quantity += 1
#             elif action == 'minus' and cart_item.quantity > 1:
#                 cart_item.quantity -= 1
            
#             # Update total amount
#             cart_item.total_amt = cart_item.quantity * cart_item.product.psellprice
#             cart_item.save()
            
#             messages.success(request, 'Cart quantity updated')
#         except Cart.DoesNotExist:
#             messages.error(request, 'Product not found in cart')
    
#     return redirect('cart_list')




# from django.contrib import messages

# def registration(request):
#     email = request.session.get('email')
#     print("Registering user with email:", email)  # DEBUG

#     if not email:
#         messages.error(request, "Session expired. Please try again.")
#         return redirect('send_otp')

#     if request.method == 'POST':
#         first = request.POST['first']
#         last = request.POST['last']
#         mobile = request.POST['mobile']
#         gender = request.POST['gender']
        
#         password = request.POST['password']

#         if Customer.objects.filter(email=email).exists():
#             messages.error(request, "User already exists. Please login.")
#             return redirect('send_otp')

#         # Save user
#         customer = Customer.objects.create(
#             first=first,
#             last=last,
#             email=email,
#             mobile=mobile,
#             gender=gender,
#             password=password  # You may hash this later!
#         )

#         request.session['customer_id'] = customer.id
#         messages.success(request, "Account created successfully!")
#         return redirect('profile')  # or 'account'

#     return render(request, 'web_html/register.html', {'email': email})


# def contact(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')

#         # Optional: save to DB or send email here
#         print(f"Name: {name}, Email: {email}, Message: {message}")

#         messages.success(request, 'Your message has been sent successfully!')
#         return redirect('contact')  # Reload the same page with success message

#     return render(request, 'web_html/contact.html')





# from django.shortcuts import render
# from .models import Product  # or whatever your product model is called

# def search(request):
#     query = request.GET.get('query')
#     results = []

#     if query:
#         results = Product.objects.filter(name__icontains=query)  # Add more fields if needed

#     return render(request, 'web/search_results.html', {'query': query, 'results': results})

# import random
# from django.core.mail import send_mail
# from django.shortcuts import render, redirect
# from django.contrib import messages

# # Store OTP temporarily (use session in real app)
# otp_storage = {}

# def send_otp(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         otp = str(random.randint(100000, 999999))
#         otp_storage[email] = otp

#         # Send OTP via email
#         send_mail(
#             subject="Your OTP for Grocer Login",
#             message=f"Your OTP is {otp}",
#             from_email="yourappemail@example.com",
#             recipient_list=[email],
#             fail_silently=False,
#         )

#         request.session['email'] = email
#         return redirect('verify_otp')

#     return render(request, 'web_html/login.html')

# def verify_otp(request):
#     if request.method == "POST":
#         entered_otp = request.POST['otp']
#         email = request.session.get('email')

#         if otp_storage.get(email) == entered_otp:
#             messages.success(request, "OTP verified! You are logged in.")
#             # Here you should authenticate or create user session
#             return redirect('home')  # or any dashboard
#         else:
#             messages.error(request, "Invalid OTP.")
#             return redirect('verify_otp')

#     return render(request, 'web_html/verify_otp.html')





# def send_otp(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         otp = str(random.randint(100000, 999999))
#         print("Generated OTP:", otp)  # DEBUG

#         # Save or update OTP
#         OTPVerification.objects.update_or_create(email=email, defaults={'otp': otp})

#         # Send OTP to user's Gmail
#         send_mail(
#             'Your GrOTP Code',
#             f'Your OTP is: {otp}',
#             'yourprojectemail@example.com',
#             [email],
#             fail_silently=False,
#         )

#         request.session['email'] = email
#         print("Saved email in session:", email)  # DEBUG

#         return redirect('verify_otp')

#     return render(request, 'web_html/send_otp.html')



# def contact_submit(request):
#     if request.method == 'POST':
#         Message.objects.create(
#             name=request.POST.get('name'),
#             email=request.POST.get('email'),
#             message_text=request.POST.get('message_text')
#         )
#         return redirect('message_list')
#     return render(request, 'contact.html')



# def remove_product(request,id):
#     if request.method == 'POST':
#         user = request.user
#         cart_item = Cart.objects.get(user=user, product_id=id)
#         cart_item.delete()
#         return redirect('cart_list')
#     return redirect('cart_list')












# def shop_cart(request, id):
#     title = 'Cart Details'
#     cust_id = request.session.get('cust_id')

#     if not cust_id:
#         return redirect('login')

#     try:
#         prod = Fruit.objects.get(id=id)
#         # Check if the item is already in the cart
#         existing_cart_item = Cart.objects.filter(customer_id=cust_id, fruit_id=id, status=1).first()

#         if existing_cart_item:
#             # If item already in the cart, increase quantity
#             existing_cart_item.quantity += 1
#             existing_cart_item.total_amt = existing_cart_item.quantity * prod.fprice
#             existing_cart_item.save()
#         else:
#             # Add new item to the cart
#             Cart.objects.create(
#                 customer_id=cust_id,
#                 fruit_id=id,
#                 quantity=1,
#                 total_amt=prod.fprice
#             )

#         # Fetch updated cart data
#         cart_data = Cart.objects.filter(customer_id=cust_id, status=1)
#         total_item = len(cart_data)

#         return render(request, 'web_html/cart.html', {'title': title, 'cart_data': cart_data, 'total_item': total_item})

#     except Fruit.DoesNotExist:
#         messages.error(request, 'Fruit not found')
#         return redirect('shop')







    

# def cart(request, id):
#     title = 'Cart Details'
#     cust_id = request.session.get('cust_id')
    
#     if not cust_id:
#         return redirect('login')

#     try:
#         prod = Product.objects.get(id=id)
        
#         # Check if the product is already in the cart
#         existing_cart_item = Cart.objects.filter(
#             customer_id=cust_id, 
#             product_id=id, 
#             status=1
#         ).first()
        
#         if existing_cart_item:
#             # If product exists, increase quantity
#             existing_cart_item.quantity += 1
#             existing_cart_item.total_amt = existing_cart_item.quantity * prod.psellprice
#             existing_cart_item.save()
#         else:
#             # Create new cart item
#             Cart.objects.create(
#                 customer_id=cust_id,
#                 product_id=id,
#                 quantity=1,
#                 total_amt=prod.psellprice
#             )
        
#         # Fetch updated cart data
#         cart_data = Cart.objects.filter(customer_id=cust_id, status=1)
        
#         # Calculate totals
#         total_original_price = sum(cart_item.product.pprice * cart_item.quantity for cart_item in cart_data)
#         total_cart_amount = sum(cart_item.product.psellprice * cart_item.quantity for cart_item in cart_data)
        
#         # Calculate discount
#         total_discount = total_original_price - total_cart_amount
        
#         # Tax calculation (adjust as per your requirements)
#         tax_percentage = 10  # Set your tax rate here
#         tax_amount = total_cart_amount * (tax_percentage / 100)
        
#         # Final total
#         final_total = total_cart_amount + tax_amount
        
#         # Total items in cart
#         total_item = cart_data.count()
        
#         return render(request, 'web_html/cart.html', {
#             'title': title,
#             'cart_data': cart_data,
#             'total_item': total_item,
#             'total_original_price': round(total_original_price, 2),
#             'total_cart_amount': round(total_cart_amount, 2),
#             'total_discount': round(total_discount, 2),
#             'tax_amount': round(tax_amount, 2),
#             'final_total': round(final_total, 2)
#         })
            
#     except Product.DoesNotExist:
#         # Handle case where product is not found
#         messages.error(request, 'Product not found')
#         return redirect('home')

