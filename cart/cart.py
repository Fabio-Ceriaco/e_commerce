from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        #get request
        self.request = request
        # Get the current session key if exists
        
        cart = self.session.get('session_key')
        
        # if the user is new, no session key! create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        # make sure cart is available on all pages of site
        self.cart = cart
        
    def add(self, product, quantity):
        product_id = str(product.id)
        product_quantity = str(quantity)
        
        #logic 
        
        if product_id in self.cart: # check if product is in cart already if is pass if not add
            pass
        else:
            # self.cart[product_id] = {'price' : str(product.price), 'quantity' : int(product_quantity)}
            self.cart[product_id] = int(product_quantity)
        self.session.modified = True
        
        # deal with logged in user
        if self.request.user.is_authenticated:
            # Get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert single to double quotations in cart dictionary ex: form {'1' : 2, '3' : 4} to {"1" : 2, "3" : 4}
            new_cart = str(self.cart)
            new_cart = new_cart.replace("\'", "\"")
            # Save cart to the Profile model
            current_user.update(old_cart=str(new_cart))
        
    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        #get ids from cart
        product_id = self.cart.keys()
        # use id to lookup products in DB
        products = Product.objects.filter(id__in= product_id)
        
        return products
    
    def get_quantities(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_quantity = int(quantity)
        
        # get cart
        our_cart = self.cart
        #update dict cart
        our_cart[product_id] = product_quantity
        
        self.session.modified = True
        
        # deal with logged in user
        if self.request.user.is_authenticated:
            # Get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert single to double quotations in cart dictionary ex: form {'1' : 2, '3' : 4} to {"1" : 2, "3" : 4}
            new_cart = str(self.cart)
            new_cart = new_cart.replace("\'", "\"")
            # Save cart to the Profile model
            current_user.update(old_cart=str(new_cart))
        
        return self.cart
    
    def delete(self, product):
        product_id = str(product)
        our_cart = self.cart
        
        if product_id in our_cart:
            # del our_cart[product_id]
            our_cart.pop(product_id)
        self.session.modified = True
        
        # deal with logged in user
        if self.request.user.is_authenticated:
            # Get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert single to double quotations in cart dictionary ex: form {'1' : 2, '3' : 4} to {"1" : 2, "3" : 4}
            new_cart = str(self.cart)
            new_cart = new_cart.replace("\'", "\"")
            # Save cart to the Profile model
            current_user.update(old_cart=str(new_cart))
        
    def cart_total(self):
        # get products id
        quantities = self.cart
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        total = 0
        
        for key, value in quantities.items():
            key = int(key)
            
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += (product.sale_price * value)
                    else:
                        total += (product.price * value)
        return total
        
    def db_add(self, product, quantity):
        product_id = str(product)
        product_quantity = str(quantity)
        
        #logic 
        
        if product_id in self.cart: # check if product is in cart already if is pass if not add
            pass
        else:
            # self.cart[product_id] = {'price' : str(product.price), 'quantity' : int(product_quantity)}
            self.cart[product_id] = int(product_quantity)
        self.session.modified = True
        
        # deal with logged in user
        if self.request.user.is_authenticated:
            # Get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert single to double quotations in cart dictionary ex: form {'1' : 2, '3' : 4} to {"1" : 2, "3" : 4}
            new_cart = str(self.cart)
            new_cart = new_cart.replace("\'", "\"")
            # Save cart to the Profile model
            current_user.update(old_cart=str(new_cart))
        
        
        