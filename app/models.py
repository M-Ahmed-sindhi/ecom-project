from django.db import models
import datetime
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    
    

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default="", blank=True, null=True)
    image = models.ImageField(upload_to="product/")
    on_sale = models.BooleanField(default=False)
    if_sale = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(
        Product,  # Remove the string reference, use the actual model
        on_delete=models.CASCADE,
        related_name='app_orders'  # Keep the unique related_name
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=20, default="")
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.customer}"


# Create your models here.