from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('contact/',views.contact,name='contact'),
    path('registration/',views.registration,name='registration'),
    path('loginwithgamil/',views.loginwithgamil,name='loginwithgmail'),
    path('login/',views.login,name='login'),
    path('wishlist/',views.wishlist,name='wishlist'),
    # path('cart/<id>',views.cart,name='cart'),
    path('cart_list/',views.cart_list,name='cart_list'),
    path('cleaning/',views.cleaning,name='cleaning'),
    path('table/',views.table,name='table'),
    path('edit_cust/<id>',views.edit_cust,name='edit_cust'),
    path('del_cust/<id>',views.del_cust,name='del_cust'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    # path('shop_cart/<id>',views.shop_cart,name='shop_cart'),
    path('shop/',views.shop,name ='shop'),
    # path('remove_product/<int:id>/', views.remove_product, name='remove_product'),
    path('remove_product/<int:id>/', views.remove_product, name='remove_product'),
    path('update_cart_quantity/<int:id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('deliveryone/',views.deliveryone,name='deliveryone'),
    path('payment/',views.payment,name='payment'),
    path('about/',views.about,name='about'),
    # path('add-to-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove-from-wishlist/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('move-to-cart/<int:id>/', views.move_to_cart, name='move_to_cart'),
    path('update_cart_quantity/<int:id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('update-cart/<int:id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('list/', views.list, name='list'),
    path('contact/', views.contact, name='contact'),

    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    
   path('my_orders/', views.my_orders, name='my_orders'),
   path('place_order/', views.place_order, name='place_order'),
   path('order_success/', views.order_success, name='order_success'),
   
path('order-history/', views.order_history, name='order_history'),
    path('add-to-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('order/track/<int:order_id>/', views.track_order, name='track_order'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order/invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    path('search/', views.search_products, name='search_products'),
    path('save_address/', views.save_address, name='save_address'),
    path('category/<int:cat_id>/', views.category_products, name='category_products'),
    path('add-to-cart/<str:item_type>/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_quantity/<int:id>/',views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/', views.cart_list, name='cart_list')

]

# path('signup/email/', views.send_otp_view, name='send_otp'),
    # path('signup/verify/', views.verify_otp_view, name='verify_otp'),
    # path('registration/', views.registration, name='registration'),
    # path('send-otp/', views.send_otp, name='send_otp'),
    # path('verify-otp/', views.verify_otp, name='verify_otp'),
    # path('register/', views.registration, name='registration'),
    # path('', views.home, name='home'), 
# path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
# path('contact/', views.contact_submit, name='contact_submit'),
#    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    # path('search/', views.search, name='search'),