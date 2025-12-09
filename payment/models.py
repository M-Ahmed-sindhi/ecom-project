from django.db import models
from django.contrib.auth.models import User
from app.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime
from django.utils import timezone

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_email = models.EmailField(max_length=100, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=100, null=True, blank=True)
    shipping_address = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=100, null=True, blank=True)
    shipping_postal_code = models.CharField(max_length=20, null=True, blank=True)
    shipping_state = models.CharField(max_length=100, null=True, blank=True)
    shipping_country = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        return f"{self.shipping_full_name} - {self.shipping_city}"
    
    def create_shipping_address(sender, instance, created, **kwargs):
        if created:
            shipping_user = ShippingAddress(user=instance)
            shipping_user.save()

post_save.connect(ShippingAddress.create_shipping_address, sender=User)
class p_Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250, null=True)
    email = models.EmailField(max_length=250, null=True)
    shipping_address = models.TextField(max_length=15000, null=True)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    shipped = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
		      return f'Order - {str(self.id)}'

# Auto Add shipping Date
@receiver(pre_save, sender=p_Order)
def set_date_shipped(sender, instance, **kwargs):
    if instance.pk:  # only for updates
        obj = sender.objects.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = timezone.now()
    else:  # for new orders
        if instance.shipped:
            instance.date_shipped = timezone.now()


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey('p_Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"