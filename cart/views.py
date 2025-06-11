from django.shortcuts import render, get_object_or_404
from .cart import Cart
from django.contrib import messages
from store.models import Product, Category
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    categories = Category.objects.all()
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {'products' : cart_products, 'quantities' : quantities, 'totals' : totals, 'categories' : categories})

def cart_add(request):
    # get cart
    cart = Cart(request)
    #test for POST
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        #lookup product in DB
        product = get_object_or_404(Product, id=product_id)
        # save to session
        cart.add(product=product, quantity=product_quantity)
        
        cart_quantity = cart.__len__()
        # return response
        # response = JsonResponse({'Product Name' : product.name})
        response = JsonResponse({'qty' : cart_quantity})
        messages.success(request, ('Product add to cart'))
        
        return response
        

def cart_delete(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product' : product_id})
        messages.success(request, ('Product deleted from cart'))
        return response

def cart_update(request):
    cart = Cart(request)
    #test for POST
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = str(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        cart.update(product=product_id, quantity= product_quantity)
        response = JsonResponse({'qty' : product_quantity})
        messages.success(request, ('Cart updated!'))
        return response
        # return redirect('cart:cart')
