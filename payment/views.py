from django.shortcuts import render, redirect
from cart.cart import Cart
from store.models import Category, Profile
from .models import ShippingAddress, Order, OrderItem
from .forms import ShippingForm, PaymentForm
from store.models import Product
from django.contrib import messages
from django.contrib.auth.models import User
import datetime

# Create your views here.
def payment_success(request):
    
    return render(request, 'payment_success.html', {})

def checkout(request):
    cart = Cart(request)
    categories = Category.objects.all()
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    totals = cart.cart_total()
    #checkout as logged in user
    if request.user.is_authenticated:
        #get current users shipping user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #get user shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'checkout.html', {'products' : cart_products, 'quantities' : quantities, 'totals' : totals, 'categories' : categories, 'shipping_form' : shipping_form})
    else: 
        # checkout as guess
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'checkout.html', {'products' : cart_products, 'quantities' : quantities, 'totals' : totals, 'categories' : categories, 'shipping_form' : shipping_form})
    
def billing_info(request):
    if request.POST:
        cart = Cart(request)
        categories = Category.objects.all()
        cart_products = cart.get_products()
        quantities = cart.get_quantities()
        totals = cart.cart_total()
        # Create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        
        # check if user is logged in
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'billing_info.html', {'products' : cart_products, 'quantities' : quantities, 'totals' : totals, 'categories' : categories, 'shipping_info' : request.POST, 'billing_form' : billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'billing_info.html', {'products' : cart_products, 'quantities' : quantities, 'totals' : totals, 'categories' : categories, 'shipping_info' : request.POST, 'billing_form' : billing_form})
        
    else:
        messages.error(request, ('Access Denied.'))
        return redirect('store:home')
    
def process_order(request):
    if request.POST:
        cart = Cart(request)
        categories = Category.objects.all()
        cart_products = cart.get_products()
        quantities = cart.get_quantities()
        totals = cart.cart_total()
        # Get Billing Info from Last Page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping session Data
        my_shipping = request.session.get('my_shipping')
        
        # Gather order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        
        #  Create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals
        #Create an Order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            # Add Order Items
            # get product info
            for product in cart_products:
                # get product price
                if not product.is_sale:
                    product_price = product.price
                else:
                    product_price = product.sale_price
                # Get quantity
                for key, value in quantities.items():
                    if int(key) == product.id:
                            # Create Order Item
                            create_order_item = OrderItem(order=create_order, product=product, user=user, quantity=value, price=product_price)
                            create_order_item.save()
            # Delete our cart
            
            for key in list(request.session.keys()):
                if key == 'session_key':
                    # Delete the key
                    del request.session[key]
                    
            # Delete cart from database
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database
            current_user.update(old_cart='')
            
            messages.success(request, ('Order Placed.'))
            return redirect('store:home')
            
        else:
            # no logged user
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            # Add Order Items
            # get product info
            for product in cart_products:
                # get product price
                if not product.is_sale:
                    product_price = product.price
                else:
                    product_price = product.sale_price
                # Get quantity
                for key, value in quantities.items():
                    if int(key) == product.id:
                            # Create Order Item
                            create_order_item = OrderItem(order=create_order, product=product, quantity=value, price=product_price)
                            create_order_item.save()
                            
            # Delete our cart
            for key in list(request.session.keys()):
                if key == 'session_key':
                    # Delete the key
                    del request.session[key]
                            
            messages.success(request, ('Order Placed.'))
            return redirect('store:home')
        
    else:
        messages.error(request, ('Access Denied.'))
        return redirect('store:home')
    
def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # get the order
            order = Order.objects.filter(id=num)
            # update the status
            order.update(shipped=True, date_shipped=datetime.datetime.now())
            messages.success(request, ('Shipping status updated.'))
            return redirect('store:home')
            
        return render(request, 'not_shipped_dash.html', {'orders' : orders})
    else:
        messages.error(request, ('Access Denied'))
        return redirect('store:home')
    
def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            
            # get the order
            order = Order.objects.filter(id=num)
            # update the status
            order.update(shipped=False)
            messages.success(request, ('Shipping status updated.'))
            return redirect('store:home')
            
        return render(request, 'shipped_dash.html', {'orders' : orders })
    else:
        messages.error(request, ('Access Denied'))
        return redirect('store:home')
    
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        
        # Get Order Items
        items = OrderItem.objects.filter(order=pk)
        if request.POST:
            status = request.POST['shipping_status']
            
            # Check if true or false
            if status == 'true':
                # get the order
                order = Order.objects.filter(id=pk)
                # update the status
                order.update(shipped=True, date_shipped=datetime.datetime.now())
                messages.success(request, ('Shipping status updated.'))
                return redirect('store:home')
            else:
                # get the order
                order = Order.objects.filter(id=pk)
                # update the status
                order.update(shipped=False)
                messages.success(request, ('Shipping status updated.'))
                return redirect('store:home')
                
        return render(request, 'orders.html', {'order' : order, 'items' : items})
    else:
        messages.error(request, ('Access Denied'))
        return redirect('store:home')