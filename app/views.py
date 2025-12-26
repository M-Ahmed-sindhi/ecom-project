from django.shortcuts import render, redirect,  get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, updateUserForm, changepasswordForm, UserInfoForm
from django import forms
from cart.cart import Cart
from payment.forms import ShippingAddressForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from payment.models import ShippingAddress
import json


def update_info(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must log in first')
        return redirect('login')

    profile = Profile.objects.get(user=request.user)
    shipping_user = ShippingAddress.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = UserInfoForm(request.POST, instance=profile)
        shipping_form = ShippingAddressForm(request.POST, instance=shipping_user)
        
        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_instance = shipping_form.save(commit=False)
            shipping_instance.user = request.user
            shipping_instance.save()
            messages.success(request, "Your info is updated")
            return redirect('image')
    else:
        form = UserInfoForm(instance=profile)
        shipping_form = ShippingAddressForm(instance=shipping_user)

    return render(request, "update_info.html", {"form": form, "shipping_form": shipping_form})



def update_password(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must log in first')
        return redirect('login')

    if request.method == "POST":
        form = changepasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # critical to keep session valid
            messages.success(request, "Password updated successfully")
            return redirect('image')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('update_password')
    else:
        form = changepasswordForm(request.user)
    return render(request, "update_password.html", {"form": form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(pk=request.user.id)
        form = updateUserForm(instance=current_user)

        if request.method == "POST":
            form = updateUserForm(request.POST, instance=current_user)
            if form.is_valid():
                form.save()
                login(request, current_user)
                messages.success(request, "Profile updated")
                return redirect('image')

        return render(request, "update_user.html", {"form": form})
    else:
        messages.error(request, 'You must log in first')
        return redirect('login')




def category_summary(request):
     categories = Category.objects.all()
     return render(request, "category_summary.html", {"categories": categories})

# Create your views here.
def image(request):
    products = Product.objects.only('id', 'name', 'price', 'is_sale', 'sale_price', 'image').all().iterator()
    return render(request, "index.html", {'products':products})

def about(request):
    return render(request, "about.html", {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            profile = Profile.objects.filter(user=user).first()

            if profile and profile.old_cart:
                try:
                    request.session['cart'] = json.loads(profile.old_cart)
                except json.JSONDecodeError:
                 pass
                profile.old_cart = ""
                profile.save()

            messages.success(request, "You have been logged in")
            return redirect("image")


            
            
    else:
        return render(request, "login.html", {})  # show page on GET

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("image")

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are registered")
                return redirect("image")
            else:
                messages.error(request, "Authentication failed")
                return redirect("login")
        else:
            messages.error(request, "There was a problem with your registration")
            return redirect("register")
    else:
        form = SignUpForm()
    return render(request, "register.html", {"form": form})
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product.html", {"product": product})

def category(request, bob):
    bob = bob.replace("-", " ")  # replace hyphens with spaces
    try:
        
        category = Category.objects.get ( name=bob)
        products = Product.objects.filter(category=category).only('id', 'name', 'price', 'is_sale', 'sale_price', 'image').iterator()
        return render(request, "category.html", {'products':products, 'category':category})

    except:
        messages.error(request, "No such category")
        return redirect("image")
    
def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query).only('id', 'name', 'price', 'description', 'image') if query else []
    return render(request, "search_results.html", {'products': products, 'query': query})
  
