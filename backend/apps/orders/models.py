from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.core.models import TimeStampedModel
from apps.authentication.models import User
from apps.products.models import Product, ProductVariant


class Order(TimeStampedModel):
    """Order model for storing customer orders."""

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("processing", _("Processing")),
        ("shipped", _("Shipped")),
        ("delivered", _("Delivered")),
        ("cancelled", _("Cancelled")),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("paid", _("Paid")),
        ("failed", _("Failed")),
        ("refunded", _("Refunded")),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        help_text=_("User who placed the order"),
    )
    order_number = models.CharField(
        _("order number"),
        max_length=50,
        unique=True,
        help_text=_("Unique order identifier"),
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text=_("Current order status"),
    )
    payment_status = models.CharField(
        _("payment status"),
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
        help_text=_("Payment status"),
    )
    
    # Shipping Information
    shipping_first_name = models.CharField(
        _("first name"), max_length=150, help_text=_("Shipping first name")
    )
    shipping_last_name = models.CharField(
        _("last name"), max_length=150, help_text=_("Shipping last name")
    )
    shipping_email = models.EmailField(
        _("email"), help_text=_("Shipping email address")
    )
    shipping_phone = models.CharField(
        _("phone"), max_length=20, help_text=_("Shipping phone number")
    )
    shipping_address = models.CharField(
        _("address"), max_length=255, help_text=_("Street address")
    )
    shipping_city = models.CharField(
        _("city"), max_length=100, help_text=_("City")
    )
    shipping_state = models.CharField(
        _("state"), max_length=100, help_text=_("State/Province")
    )
    shipping_postal_code = models.CharField(
        _("postal code"), max_length=20, help_text=_("Postal/ZIP code")
    )
    shipping_country = models.CharField(
        _("country"), max_length=100, help_text=_("Country")
    )
    
    subtotal = models.DecimalField(
        _("subtotal"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text=_("Order subtotal"),
    )
    shipping_cost = models.DecimalField(
        _("shipping cost"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text=_("Shipping cost"),
    )
    total = models.DecimalField(
        _("total"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text=_("Order total"),
    )
    notes = models.TextField(
        _("notes"), blank=True, help_text=_("Order notes from customer")
    )
    tracking_number = models.CharField(
        _("tracking number"),
        max_length=100,
        blank=True,
        help_text=_("Shipping tracking number"),
    )

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["user", "status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        """Return string representation of the order."""
        return f"Order #{self.order_number}"

    def calculate_total(self):
        """Calculate order total."""
        return self.subtotal + self.shipping_cost


class OrderItem(TimeStampedModel):
    """Order item model for storing products in orders."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        help_text=_("Order this item belongs to"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        help_text=_("Product ordered"),
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="order_items",
        help_text=_("Product variant ordered"),
    )
    quantity = models.PositiveIntegerField(
        _("quantity"),
        validators=[MinValueValidator(1)],
        help_text=_("Quantity ordered"),
    )
    price = models.DecimalField(
        _("price"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text=_("Price per unit at time of order"),
    )

    class Meta:
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order", "product"]),
        ]

    def __str__(self):
        """Return string representation of the order item."""
        return f"{self.quantity}x {self.product.name} in Order #{self.order.order_number}"

    @property
    def total_price(self):
        """Calculate total price for this item."""
        # Защита от None значений
        if self.price is None or self.quantity is None:
            return Decimal("0.00")
        return Decimal(str(self.price)) * self.quantity