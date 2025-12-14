
from .cart import Cart  # or adjust import path if Cart lives elsewhere

def cart_processor(request):
    return {'cart': Cart(request)}