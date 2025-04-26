from . import views
from django.urls import path

urlpatterns = [
    path('',views.admin,name='admin'),
    path('AddProduct/',views.add_product,name='add_product'),
    path('ProductList/',views.product_list,name='product_list'),
    path('Category/',views.Categoryy,name='Category'),
    path('fruits/',views.fruits,name='fruits'),
    path('menu/',views.menu,name='menu'),
   path('contact-messages/', views.contact_messages, name='contact_messages'),
   path('all_orders/', views.all_orders, name='all_orders'),
path('confirm_order/<int:id>/', views.confirm_order, name='confirm_order'),
path('shipped_order/<int:id>/', views.shipped_order, name='shipped_order'),
   path('delivered_order/<int:order_id>/', views.delivered_order, name='delivered_order'),
    path('order/shipped/<int:order_id>/', views.shipped_order, name='shipped_order'),
]