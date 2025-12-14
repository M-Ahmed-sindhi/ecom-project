from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .cart import Cart
from app.models import Product  
from django.http import JsonResponse 
from app.models import Product



def cart_summary(request):
    cart = Cart(request)
    print("CART CONTENTS:", cart.cart)  # Debug line
    cart_products = cart.get_products()
    cart_quantity = cart.get_qun
    totals = cart.total()
    print("CART PRODUCTS:", cart_products)  # Debug line
    return render(request, 'cart/cart_summary.html', {'cart_products': cart_products, 'cart_quantity': cart_quantity, 'totals': totals})

def cart_add(request):
    if request.method == 'POST':
        try:
            product_id = int(request.POST.get('product_id'))
            cart = Cart(request)
            product = get_object_or_404(Product, id=product_id)
            product_quantity = int(request.POST.get('quantity', 1))
            cart.add(product=product, quantity=product_quantity)
            
            return JsonResponse({
                'success': True, 
                'product_name': product.name,
                'cart_count': cart.__len__()
            })
        
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid product ID'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
    


   
def cart_delete(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')

            if not product_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Missing product_id'
                }, status=400)

            cart = request.session.get('cart', {})

            if product_id in cart:
                del cart[product_id]
                request.session['cart'] = cart
                request.session.modified = True

                return JsonResponse({
                    'success': True,
                    'message': 'Product removed successfully',
                    'cart_total': len(cart)
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
            }, status=500)

    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)

       
def cart_update(request):
    
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')
            quantity = request.POST.get('quantity')
            
            # Get the cart
            cart = request.session.get('cart', {})
            
            # Update the quantity
            if product_id and quantity:
                cart[product_id] = int(quantity)
                request.session['cart'] = cart
                request.session.modified = True
                
                return JsonResponse({
                    'success': True,
                    'message': 'Cart updated successfully',
                    'cart_total': len(cart)
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Missing product_id or quantity'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)


    
    #cart = Cart(request)
   # if request.method == 'POST':
    
      
    """ product_id = request.POST.get('product_id')
        product_quantity = request.POST.get('quantity')
        
        cart.update(product=product_id, quantity=product_quantity)
        return JsonResponse({
            'success': True,
            'cart_count': cart.__len__()
        })
        return redirect('cart:cart_summary')
    """


# Create your views here.
