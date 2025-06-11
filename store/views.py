from django.shortcuts import render, redirect
from django.http import Http404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordFrom, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django.core.signing import Signer # encrypt string
from django.core import signing # exception error Signer
from django.contrib.auth.models import User
from django.db.models import Q
import json
from cart.cart import Cart

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    signer = Signer()  #instaciar a class
    for product in products:
        product.signed_id = signer.sign(product.id) # associar id do produto cryptado coleção de produtos
    return render(request, 'home.html', {'products' : products, 'categories' : categories})

def about(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {'categories' : categories})

def login_user(request):
    categories = Category.objects.all()
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Do some shopping cart stuff
                current_user = Profile.objects.get(user__id=request.user.id)
                # Get save cart from db
                saved_cart = current_user.old_cart
                # convert dad+tabase string to python dictionary
                if saved_cart:
                    #convert to dictionary using JSON
                    converted_cart = json.loads(saved_cart)
                    # add the loaded cart dictionary to session
                    cart = Cart(request)
                    # loop to cart add items fom database
                    for key, value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)
                        
                messages.success(request, ('You have been logged in!'))
                return redirect('store:home')
            else:
                messages.error(request, ('Invalid login!'))
                return redirect('store:login')
        else:
            return render(request, 'login.html', {'categories' : categories})
    else:
        return redirect('store:home')
        
def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out... Thanks!'))
    return redirect('store:home')

def register_user(request):
    categories = Category.objects.all()
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Username Created -  Please Fill Out Your User Info Below.'))
            return redirect('store:update_info')
        else:
            form = SignUpForm()
            return render(request, 'register.html', {'form' : form})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form' : form, 'categories' : categories })

def product(request, signed_id):
    categories = Category.objects.all()
    signer = Signer()
    try:  # descryptar o id
        pk = signer.unsign(signed_id)
    except signing.BadSignature:
        raise Http404('Invalid product link.')
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product' : product, 'categories' : categories})

def category(request, category):
    categories = Category.objects.all()
    category = category.replace('-', ' ')
    try:
        category = Category.objects.get(name=category)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products' : products, 'category' : category, 'categories' : categories})
    except:
        messages.error(request, ("That category doesn't exist!"))
        return redirect('store:home')
    
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories' : categories})

def user_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            
            messages.success(request, ('User has been updated.'))
            return redirect('store:home')
        
        return render(request, 'user_profile.html', {'user_form' : user_form})
    else:
        messages.error(request, ('You must be logged in to access that page!'))
        return redirect('store:home')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        
        # did they fill out the form
        
        if request.method == 'POST':
            form = ChangePasswordFrom(current_user, request.POST)
            if form.is_valid():
                form.save()
                login(request, current_user)
                messages.success(request, ('Your password as been updated!'))
                return redirect('store:home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('store:update_password')
        else:
            form = ChangePasswordFrom(current_user)
            return render(request, 'update_password.html', {'form' : form })
    else:
        messages.error(request, ('You must be logged in to access that page!'))
        return redirect('store:home')
    
def update_info(request):
    if request.user.is_authenticated:
        # current_user = User.objects.get(id=request.user.id)
        current_user = Profile.objects.get(user__id=request.user.id)
        
        #get current users shipping user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        
        # get original user form
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        #get user shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            # save original form
            form.save()
            #save shipping form
            shipping_form.save()
            
            messages.success(request, ('Your info has been update!'))
            return redirect('store:home')
        else:
            
            return render(request, 'update_info.html', {'form' : form, 'shipping_form' : shipping_form})
    else:
        messages.error(request, ('You must be logged in to access that page!'))
        return redirect('store:home')
            
def search_product(request):
    # Determine if they filled out the form
    if request.method == 'POST':
        search = request.POST['searched']
        # Query the products in DB model
        search = Product.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
        
        #test for null
        if not search:
            messages.error(request, ("That product doesn't exists... Please try again!"))
            return render(request, 'search_product.html', {'search' : search})
        else:
            return render(request, 'search_product.html', {'search' : search})
    else:
        return render(request, 'search_product.html', {})        
    


    