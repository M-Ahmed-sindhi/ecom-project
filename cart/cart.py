from django.core.exceptions import ObjectDoesNotExist
from app.models import Product, Profile 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt# Import here to avoid circular imports
class Cart:
    def __init__(self, request):
        self.request = request
        # get request session
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
    
    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_quantity = int(quantity)
    
        if product_id in self.cart:
            self.cart[product_id] += product_quantity
        else:
            self.cart[product_id] = product_quantity
        self.save()

    # deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("'", '"')
        # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

           
    
    def save(self):
        self.session.modified = True
    
    def __len__(self):
        return sum(self.cart.values())

    
    
    
    def clear(self):
        # Remove cart from session
        del self.session['cart']
        self.save()

    def get_products(self):
    
    # FILTER OUT EMPTY STRINGS FIRST
        product_ids = [id for id in self.cart.keys() if id and id.strip()]
        print("DEBUG - Looking for product IDs:", product_ids)  # Add this
    
        products = Product.objects.filter(id__in=product_ids)
        print("DEBUG - Found products:", [p.id for p in products])  # Add this

    
        cart_products = []
        for product in products:
            product_id = str(product.id)
            quantity = self.cart.get(product_id, 0)  # Use get() to avoid KeyError
        
            cart_products.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity,
                'image': product.image.url if product.image else '',
                'total_price': float(product.price) * quantity,
            })
    
        return cart_products


    def get_qun(self):
        quantity = self.cart
        return quantity      

    def mob(self, product_id, quantity):
        """Update product quantity in cart"""
        if quantity > 0:
            self.cart[product_id] = quantity
        else:
            # Remove if quantity is 0 or less
            self.remove(product_id)
        
        self.save()

    def get_produc(self):
    # Get cart data from session
        pouduct_ids = self.cart.keys()
        products = Product.objects.filter(id__in=pouduct_ids)
        return products
        
    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.get_productes())
    
    def update(self, product, quantity):
        product_id = str(product)
        product_quantity = int(quantity)
        
        self.cart[product_id] = product_quantity
        self.session.modified = True
        self.save()

    def delete(self, product_id):
      
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            return True
        return False
      
    def total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        cart_total = 0
        for key, quantity in quantities.items():
            key_str = str(key)
            for product in products:
                if str(product.id) == key_str:
                    if product.is_sale:
                        cart_total += product.sale_price * quantity
                    else:
                        cart_total += product.price * quantity
        return cart_total

        
        '''  try:
            product_id = request.POST.get('product_id')
        
            if not product_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Product ID is required'
             }, status=400)
        
        # Get the cart from session
            cart = request.session.get('cart', {})
        
            # Remove the product from cart
            if product_id in cart:
                del cart[product_id]
                request.session['cart'] = cart
                request.session.modified = True
            
                return JsonResponse({
                    'success': True,
                    'message': 'Product removed from cart',
                '   cart_count': len(cart)
             })
            else:
                return JsonResponse({
                'success': False,
                'error': 'Product not found in cart'
                }, status=404)
            
        except Exception as e:
            return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)'''
        
  

    