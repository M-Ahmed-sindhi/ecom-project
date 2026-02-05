from djongo import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from bson.decimal128 import Decimal128
import decimal

class MongoDecimalField(models.DecimalField):
    def to_python(self, value):
        if hasattr(value, 'to_decimal'):
            return value.to_decimal()
        if isinstance(value, float):
            return self.context.create_decimal_from_float(value)
        try:
             return decimal.Decimal(value)
        except (decimal.InvalidOperation, TypeError):
             return super().to_python(value)



class ShippingAddress(models.Model):
    """Shipping address model for users"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='shipping_addresses',
        null=True, 
        blank=True
    )
    shipping_email = models.EmailField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name=_("Email")
    )
    shipping_full_name = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name=_("Full Name")
    )
    shipping_address = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
        verbose_name=_("Address")
    )
    shipping_city = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name=_("City")
    )
    shipping_postal_code = models.CharField(
        max_length=20, 
        null=True, 
        blank=True,
        verbose_name=_("Postal Code")
    )
    shipping_state = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name=_("State/Province")
    )
    shipping_country = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name=_("Country")
    )
    
    # MongoDB-specific fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Shipping Address")
        verbose_name_plural = _("Shipping Addresses")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.shipping_full_name or 'Unknown'} - {self.shipping_city or 'No City'}"

    def clean(self):
        """Validation for MongoDB document"""
        if self.shipping_email and '@' not in self.shipping_email:
            raise ValidationError({'shipping_email': _('Enter a valid email address.')})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_default_shipping_address(sender, instance, created, **kwargs):
    """Create a default shipping address when a user is created"""
    if created:
        ShippingAddress.objects.create(user=instance)


class OrderItem(models.Model):
    """Abstract model for order items - stored as embedded documents in MongoDB"""
    # Use CharField for product_id to avoid type issues with MongoDB
    product_id = models.CharField(max_length=100)
    product_name = models.CharField(
        max_length=255,
        verbose_name=_("Product Name")
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantity")
    )
    price = MongoDecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Price")
    )
    
    # Add metadata for better querying
    unit_price = MongoDecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Unit Price"),
        default=0.00
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    @property
    def total_price(self):
        """Calculate total price for this item"""
        return self.quantity * self.price

    def clean(self):
        """Validate order item data"""
        if self.quantity < 1:
            raise ValidationError({'quantity': _('Quantity must be at least 1.')})
        if self.price < 0:
            raise ValidationError({'price': _('Price cannot be negative.')})


class p_Order(models.Model):
    """Main order model using MongoDB ArrayField for embedded items"""
    
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PAID = 'paid', _('Paid')
        SHIPPED = 'shipped', _('Shipped')
        DELIVERED = 'delivered', _('Delivered')
        CANCELLED = 'cancelled', _('Cancelled')
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='orders',
        null=True, 
        blank=True
    )
    full_name = models.CharField(
        max_length=250,
        verbose_name=_("Full Name")
    )
    email = models.EmailField(
        max_length=250,
        verbose_name=_("Email")
    )
    shipping_address = models.TextField(
        max_length=1500,  # Reduced from 15000 for better MongoDB performance
        verbose_name=_("Shipping Address")
    )
    amount_paid = MongoDecimalField(
        max_digits=10,  # Increased for better flexibility
        decimal_places=2,
        verbose_name=_("Amount Paid")
    )
    
    # Use TextChoices for better type safety
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name=_("Status")
    )
    
    # MongoDB-friendly fields
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_shipped = models.DateTimeField(null=True, blank=True)
    date_delivered = models.DateTimeField(null=True, blank=True)
    
    # ArrayField for embedded MongoDB documents
    items = models.ArrayField(
        model_container=OrderItem,
        default=list,
        verbose_name=_("Order Items")
    )
    
    # Additional metadata
    shipping_cost = MongoDecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Shipping Cost")
    )
    tax_amount = MongoDecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Tax Amount")
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Order Notes")
    )
    
    # MongoDB-specific index fields
    order_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        verbose_name=_("Order Number")
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-date_ordered']
        indexes = [
            models.Index(fields=['user', 'date_ordered']),
            models.Index(fields=['status']),
            models.Index(fields=['order_number']),
        ]

    def __str__(self):
        return f"Order #{self.order_number} - {self.full_name}"

    def save(self, *args, **kwargs):
        """Generate order number and handle shipping dates"""
        if not self.order_number:
            # Generate a unique order number (MongoDB-friendly)
            import uuid
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        # Handle status transitions
        original = None
        if self.pk:
            try:
                original = p_Order.objects.get(pk=self.pk)
            except p_Order.DoesNotExist:
                original = None
        
        # Set shipping date when status changes to shipped
        if original and original.status != self.status:
            if self.status == self.OrderStatus.SHIPPED and not self.date_shipped:
                self.date_shipped = timezone.now()
            elif self.status == self.OrderStatus.DELIVERED and not self.date_delivered:
                self.date_delivered = timezone.now()
        
        super().save(*args, **kwargs)

    def clean(self):
        """Validate order data"""
        if self.amount_paid < 0:
            raise ValidationError({'amount_paid': _('Amount paid cannot be negative.')})
        
        # Validate items if provided
        if hasattr(self, 'items') and self.items:
            total_items_price = sum(item.total_price for item in self.items)
            if self.amount_paid < total_items_price:
                raise ValidationError({
                    'amount_paid': _(f'Amount paid (${self.amount_paid}) is less than '
                                    f'total items price (${total_items_price:.2f})')
                })

    @property
    def total_amount(self):
        """Calculate total order amount"""
        items_total = sum(item.total_price for item in self.items) if self.items else 0
        return items_total + self.shipping_cost + self.tax_amount

    @property
    def item_count(self):
        """Get total number of items in order"""
        return sum(item.quantity for item in self.items) if self.items else 0

    @property
    def is_shipped(self):
        """Check if order is shipped"""
        return self.status == self.OrderStatus.SHIPPED or self.status == self.OrderStatus.DELIVERED

    @property
    def shipping_date(self):
        """Get shipping date for display"""
        return self.date_shipped or self.date_ordered

    def add_item(self, product_id, product_name, quantity, price):
        """Helper method to add items to order"""
        from django.forms import model_to_dict
        
        item_data = {
            'product_id': str(product_id),  # Convert to string for MongoDB
            'product_name': product_name,
            'quantity': quantity,
            'price': price,
            'unit_price': price / quantity if quantity > 0 else 0
        }
        
        if not hasattr(self, 'items'):
            self.items = []
        
        self.items.append(OrderItem(**item_data))
        return self


# Remove the old signal and use property-based shipped field
@property
def shipped(self):
    """Backward compatibility property"""
    return self.status in [self.OrderStatus.SHIPPED, self.OrderStatus.DELIVERED]

@shipped.setter
def shipped(self, value):
    """Set shipped status with backward compatibility"""
    if value:
        self.status = self.OrderStatus.SHIPPED
    elif self.status in [self.OrderStatus.SHIPPED, self.OrderStatus.DELIVERED]:
        self.status = self.OrderStatus.PAID

# Add the property to Order class
p_Order.shipped = shipped