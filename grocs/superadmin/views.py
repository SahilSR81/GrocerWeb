from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from django.contrib import messages
from django.conf import settings

from web.models import ContactMessage
from django.core.mail import send_mail
import random


# Create your views here.
def admin(request):
    # return HttpResponse('Hello')
    title = 'Admin Dashboard'
    cat_list = Category.objects.prefetch_related('product_set').all()[0:8]
    return render(request,'superadmin/index.html',{'title':title})

def add_product(request):
    # return HttpResponse('Hello')
    title = 'Add Product'
    cat = Category.objects.filter(status=1)
    if request.method=="POST":
        pname = request.POST['pname']
        pprice = request.POST['pprice']
        psellprice = request.POST['psellprice']
        pdiscount = request.POST['pdiscount']
        pimage = request.FILES['pimage']
        description = request.POST['description']
        cats = request.POST['category']
        Product.objects.create(pname = pname,pprice = pprice, psellprice = psellprice , pdiscount=pdiscount,pimage=pimage,description=description,category_id=cats)       
        messages.info(request,"Product Added")
        return redirect('admin')

    return render(request,'superadmin/add_product.html',{'title':title,'cat_data':cat})

def product_list(request):
    title = 'Product List'
    return render(request,'superadmin/product_list.html',{'title':title})

def Categoryy(request):
    title = 'Add category'
    if request.method=="POST":
        cat_name = request.POST['cat_name']
        Category.objects.create(cat_name = cat_name)
        messages.info(request,"Category added")
        return redirect('add_product')
    return render(request,'superadmin/category.html',{'title':title})

def fruits(request):
    # return HttpResponse('Hello')
    title = 'fruits'
    cato = Menus.objects.filter(status=1)
    if request.method=="POST":
        fname = request.POST['fname']
        fprice = request.POST['fprice']
        fsellprice = request.POST['fsellprice']
        fdiscount = request.POST['fdiscount']
        fimage = request.FILES['fimage']
        fdescription = request.POST['fdescription']
        cats = request.POST['menu']
        Fruit.objects.create(fname = fname,fprice = fprice, fsellprice = fsellprice , fdiscount=fdiscount,fimage=fimage,fdescription=fdescription,menus_id=cats)       
        messages.info(request,"Product Added")
        return redirect('admin')

    return render(request,'superadmin/fruits.html',{'title':title,'cat_data':cato})

def menu(request):
    title = 'menu'
    if request.method=="POST":
        cato_name = request.POST['cato_name']
        Menus.objects.create(cato_name = cato_name)
        messages.info(request,"Category added")
        return redirect('fruits')
    return render(request,'superadmin/menu.html',{'title':title})
    
from django.shortcuts import render
from web.models import ContactMessage

def contact_messages(request):
    messages = ContactMessage.objects.all().order_by('-sent_at')
    return render(request, 'superadmin/contact_messages.html', {'messages': messages})
def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    
    return render(request, 'superadmin/all_orders.html', {'orders': orders})

def confirm_order(request, id):
    order = Order.objects.get(id=id)
    order.status = 'Confirmed'
    order.save()

    # Send email to customer
    subject = 'Your Order is Confirmed!'
    message = f"Hi {order.customer.first} {order.customer.last},\n\nYour order (ID: {order.id}) has been confirmed and is on its way!\nThanks for shopping with Grocer!"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [order.customer.email])

    messages.success(request, 'Order confirmed and customer notified.')
    return redirect('all_orders')
from django.shortcuts import render, get_object_or_404
from .models import Order

def shipped_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Shipped'
    order.save()

    return redirect('all_orders')  # or wherever you want to redirect

# superadmin/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order

def delivered_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status != 'Delivered':
        order.status = 'Delivered'
        order.save()
    return redirect('all_orders')