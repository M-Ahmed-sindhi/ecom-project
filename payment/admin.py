from django.contrib import admin
from .models import p_Order, OrderItem, ShippingAddress
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
admin.site.register(p_Order)

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
#extend p_Order admin
class p_OrderAdmin(admin.ModelAdmin):
    model = p_Order

    readonly_fields = ['date_shipped', 'amount_paid', 'user', 'full_name', 'email', 'shipping_address','date_ordered' ]  

    fields = [
          'email', 'shipping_address',
        'full_name',
        'user',
        'amount_paid',
        'shipped',
        'date_shipped',
        'date_ordered'
              # IMPORTANT
    ]
    inlines = [OrderItemInline]

  

admin.site.unregister(p_Order)
admin.site.register(p_Order, p_OrderAdmin)