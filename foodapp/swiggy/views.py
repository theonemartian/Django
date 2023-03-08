from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
import razorpay
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from .models import Cart, CartItem
from django.template import Context
from .models import Restaurant,Menu, Order, OrderItem
# Create your views here.
@login_required(login_url='signin')
def home(request):
    restaurants =Restaurant.objects.filter(status=True)
    return render(request,'restaurant_list.html',{'restaurants':restaurants})

@login_required(login_url='signin')
def restaurant_menu(request, restaurant_id):
    # Retrieve the restaurant with the given ID
    restaurant = Restaurant.objects.get(id=restaurant_id)

    # Retrieve the menu items for the restaurant
    menu_items = Menu.objects.filter(restaurant=restaurant)

    # Render the menu template with the restaurant and menu items
    context = {'restaurant': restaurant, 'menu_items': menu_items}
    return render(request, 'menu.html', context)


        
    
    
    

def register(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        name = request.POST.get('name')
        myuser=User.objects.create_user(username, email, password)
        myuser.first_name = name
        myuser.save()
        
        messages.success(request,"Registration successful")
        return redirect('signin')
                
    return render(request, 'register.html')



def signin(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            messages.success(request, f' welcome {username} !!')
            return redirect('home')
        else:
            messages.info(request, f'account done not exit plz sign in')
            return redirect('register')
    
    return render(request, 'login.html')



def logout_user(request):
    logout(request)
    return redirect('signin')







@login_required
def add_to_cart(request, restaurant_id, menuitem_id):
    item = Menu.objects.get(id=menuitem_id)
    restaurant = Restaurant.objects.get(id=restaurant_id)
    user = request.user
    
    try:
        cart = Cart.objects.get(user=user, restaurant=restaurant)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user, restaurant=restaurant)
    print(item.id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, dish_id=item ,price=item.price, dish_name=item.dish_name)
    if not created:
        cart_item.quantity += 1
        cart_item.price = item.price*cart_item.quantity
        cart_item.save()
        
    messages.success(request, f'{item.dish_name} added to cart')
    return redirect('restaurant_menu', restaurant_id=restaurant_id)

import razorpay
razorpay_client = razorpay.Client(
    auth=('rzp_test_kUPlXknSxZibly','c5w7SmSprUJHd170KjpR9aqd'))

    
@login_required
def view_cart(request):
    user = request.user
    carts = Cart.objects.filter(user=user)
    context = {'carts': carts }
    return render(request, 'cart.html', context)


def cart_delete(request):
    user = request.user
    try:
        cart = Cart.objects.filter(user=user)
        cart.delete()
        messages.success(request, 'Cart deleted.')
    except Cart.DoesNotExist:
        messages.warning(request, 'Cart does not exist.')
    return redirect('cart')


def remove_cart_item(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        messages.success(request, f'{cart_item.dish_name} removed from cart')
    return redirect('cart')



@login_required(login_url='signin')
def profile(request):
    user=request.user
    name=user.first_name
    
    orders = Order.objects.filter(user=user)
    if not user:
        return HttpResponseNotFound('Order not found')

    context = {'orders': orders,'name': name}
    return render(request, 'profile.html', context)
    
    

    
    
    

@login_required
def place_order(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    user = request.user
    amount=int(cart.get_total_price())
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')
    print(signature,"signature \n",payment_id,"paymentID")
    params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
    result=razorpay_client.utility.verify_payment_signature(params_dict)
    if result:
        cart_items=CartItem.objects.filter(cart=cart)
        
        order_items = []
        total_amount = 0
        
        order = Order.objects.create(user=user, restaurant=cart.restaurant)
        
        for item in cart_items:
            item_price = item.total_price
            total_amount = total_amount + item_price
            order_item = OrderItem(item=item.dish_id, quantity=item.quantity, price=item.price, order=order, dish_name=item.dish_name)
            order_item.save()
            order_items.append(order_item)
        
        order.total_amount = total_amount
        order.save()
        
        cart.delete()
        
        messages.success(request, 'Order placed successfully!')
        return redirect('orders')
    else:
        messages.warning(request, 'Your order was not placed')
        
        
def rzp_order(request,cart_id):
    cart = Cart.objects.get(id=cart_id)
    user=request.user
    amount= int(cart.get_total_price())*100
    amount2= int(cart.get_total_price())
    currency="INR"
    carts = Cart.objects.filter(user=user)
    payment_order=razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture=1))
    payment_order_id=payment_order['id']
    
    context={
        'amount':amount2,
        'order_id':payment_order_id,
        'carts':carts,
        'cart_id':cart_id,
        
    }
    return render(request,'checkout.html', context)
     
    
    
        
    
 


@login_required
def orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    if not orders:
        return HttpResponseNotFound('Order not found')

    context = {'orders': orders}
    return render(request, 'orders.html', context)


@login_required
def order_detail(request,order_id):
    user=request.user
    order = OrderItem.objects.filter(order=order_id)
    total_amount = Order.objects.get(id=order_id)
    if not order:
        return HttpResponseNotFound('Order not found')

    context = {'order': order , 'total':total_amount.total_amount }
    return render(request, 'order_detail.html', context)



        



