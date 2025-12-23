from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingAddressForm, BillingAddressForm
from payment.models import ShippingAddress, p_Order, OrderItem
from django.contrib import messages 
from django.contrib.auth.models import User
from app.models import Product
import datetime
from django.utils import timezone
import datetime
from django.utils import timezone

# Create your views here.

def orders(request, pk ):
      if request.user.is_authenticated and request.user.is_superuser:
          order = p_Order.objects.get(id=pk)
          orderitems = OrderItem.objects.filter(order=pk)
          if request.POST:
              status = request.POST['shipping_status']
              num = request['num']
              # check if true or false
              if status == "true":
                 order.shipped = True
                 
                 order.save()   
                 messages.success(request, "donee")
                 return redirect('image')                         
              else:
                  order.shipped = False
                  order.date_shipped = timezone.now()
                  order.save()
                  messages.success(request, "donee")
                  return redirect('image')
                  
          return render(request, "payment/orders.html",{"order": order, "orderitems": orderitems }) 
          
      else:
         messages.success(request, "access denied")
         return redirect('image')

def shipped_dash(request,):
      
      if request.user.is_authenticated and request.user.is_superuser:
        orders = p_Order.objects.filter(shipped=True)
        
         
        
        if request.method == "POST":  # Check if form was submitted
            num = request.POST.get('num')  # Get the value of 'num' from POST
            if num:  # Make sure num exists
                try:
                    # Get the order by ID, you can filter shipped=False if needed
                    order = p_Order.objects.get(id=num)  
                    order.shipped =  False
                    order.save()
                    messages.success(request, "Done!")
                except p_Order.DoesNotExist:
                    messages.error(request, "Order not found.")
         
        return render(request, "payment/shipped_dash.html",  {'orders': orders})
      else:
         messages.success(request, "access denied")
         return redirect('image')


def nshipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
         
        orders = p_Order.objects.filter(shipped=False)
       
        if request.method == "POST":  # Check if form was submitted
            num = request.POST.get('num')  # Get the value of 'num' from POST
            if num:  # Make sure num exists
                try:
                    # Get the order by ID, you can filter shipped=False if needed
                    order = p_Order.objects.get(id=num)  
                    order.shipped =  True
                    order.save()
                    messages.success(request, "Done!")
                except p_Order.DoesNotExist:
                    messages.error(request, "Order not found.")  
        return render(request, "payment/nshipped_dash.html",  {'orders': orders})
    else:
          messages.success(request, "access denied")
          return redirect('image')



def process_order(request):
    if request.method == "POST":
      cart = Cart(request)
      cart_products = cart.get_products()
      cart_quantity = cart.get_qun
      totals = cart.total()
      payment_form = BillingAddressForm(request.POST)
      my_shipping_info = request.session.get('my_shipping_info', {})
      full_name = my_shipping_info['shipping_full_name']
      email = my_shipping_info['shipping_email']
      address = my_shipping_info['shipping_address']

      shipping_address = "/".join([
    my_shipping_info.get('shipping_address', ''),
    my_shipping_info.get('shipping_city', ''),
    my_shipping_info.get('shipping_state', ''),
    my_shipping_info.get('shipping_zip_code', ''),
    my_shipping_info.get('shipping_country', ''),
])
      if request.user.is_authenticated:
         user = request.user
         create_order = p_Order(user=user,full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=totals)  
         create_order.save()
         order_id = create_order.pk

         for product in cart_products:
            
            product_id = product["id"]
            product_obj = Product.objects.get(pk=product_id)

            if product_obj.is_sale:
                price = product_obj.sale_price
            else:
                price = product_obj.price
         
            for key, value in cart_quantity().items() :
                   if str(key) == str(product["id"]):
                        create_order_item = OrderItem(
                              user=user,  
                              order=create_order,
                              product=product_obj,
                              quantity=value,
                              price=price
                        )
                        create_order_item.save()
                        #del4ete cart
            for key in list(request.session.keys()):
               if key == 'cart':
                del request.session[key]
                request.session.modified = True

         messages.success(request, "Order processed successfully")
         return redirect('image')
      else:
         user = None
         create_order = p_Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=totals)  
         create_order.save()

         for product in cart_products:
            
            product_id = product["id"]
            product_obj = Product.objects.get(pk=product_id)

            if product_obj.is_sale:
                price = product_obj.sale_price
            else:
                price = product_obj.price
         
            for key, value in cart_quantity().items():
                if str(key) == str(product["id"]):
                    create_order_item = OrderItem(
                        user=user,  
                        order=create_order,
                        product=product_obj,
                        quantity=value,
                        price=price
                    )
                    create_order_item.save()
                        
            for key in list(request.session.keys()):
                if key == 'cart':
                    del request.session[key]
                    request.session.modified = True
         messages.success(request, "Order processed successfully")
         return redirect('image')

    else:
      messages.success(request, "Invalid access to process order page")
      return redirect('image')


def billing(request): 
 if request.method == "POST":
    cart = Cart(request)
    cart_products = cart.get_products()
    cart_quantity = cart.get_qun
    totals = cart.total()
    #create aa session with shipping info
    my_shipping_info = request.POST
    request.session['my_shipping_info'] = my_shipping_info

    if request.user.is_authenticated:
       billing_form = BillingAddressForm(request.POST)
       shipping_form = request.POST
       return render(request, "payment/billing.html",  {'cart_products': cart_products, 'cart_quantity': cart_quantity, 'totals': totals, 'shipping_info': request.POST, 'billing_form': billing_form})
    else:
       pass
       billing_form = BillingAddressForm(request.POST)
    shipping_form = request.POST
    return render(request, "payment/billing.html",  {'cart_products': cart_products, 'cart_quantity': cart_quantity, 'totals': totals, 'shipping_info': request.POST, 'billing_form': billing_form})
 else:
    messages.success(request, "Invalid access to billing page")
    return redirect('image')



def payment_success(request):
   
    return render(request, "payment/payment_success.html",)


def checkouts(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    cart_quantity = cart.get_qun
    totals = cart.total()
    print("CART PRODUCTS:", cart_products)  # Debug line
    print("cart_products =", cart_products)
    print("cart_quantity =", cart_quantity)
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.filter(user=request.user).first()
        shipping_form = ShippingAddressForm(request.POST, instance=shipping_user)
        return render(request, "payment/checkout.html",  {'cart_products': cart_products, 'cart_quantity': cart_quantity, 'totals': totals, 'shipping_form': shipping_form})
    else :
       # CHeckout as guest
       shipping_form = ShippingAddressForm(request.POST, )
       return render(request, "payment/checkout.html",  {'cart_products': cart_products, 'cart_quantity': cart_quantity, 'totals': totals, 'shipping_form': shipping_form})
