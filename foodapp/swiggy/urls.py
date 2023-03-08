
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth
urlpatterns = [
   
    path('home/', views.home,name='home'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_menu, name='restaurant_menu'),
    path('register/', views.register, name='register'),
    path('', views.signin, name='signin'),
    path('logout/', views.logout_user, name ='logout'),
    path('cart/', views.view_cart, name ='cart'), 
    path('cart/delete/', views.cart_delete, name='cart_delete'),
    path('placeorder/<int:cart_id>', views.place_order, name='place_order'),
    path('cart/add/<int:restaurant_id>/<int:menuitem_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove-item/', views.remove_cart_item, name='cart_remove_item'),
    path('orders/', views.orders, name='orders'),
    path('order_detail/<int:order_id>', views.order_detail, name='order_detail'),
    path('checkout/<int:cart_id>', views.rzp_order,name='checkout'),
    path('profile/', views.profile, name='profile'),
    
]
