from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel
from apps.authentication.models import User
from apps.products.models import Product, ProductVariant


class Cart(TimeStampedModel):
    """Shopping cart model."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
        help_text=_("User who owns this cart"),
    )

    class Meta:
        verbose_name = _("cart")
        verbose_name_plural = _("carts")
        ordering = ["-created_at"]

    def __str__(self):
        """Return string representation of the cart."""
        return f"Cart for {self.user.email}"

    @property
    def total_items(self):
        """Get total number of items in cart."""
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """Calculate cart subtotal."""
        return sum(item.total_price for item in self.items.all())

    def clear(self):
        """Remove all items from cart."""
        self.items.all().delete()


class CartItem(TimeStampedModel):
    """
    Cart item model representing a product in the cart.
    """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        help_text=_("Cart this item belongs to"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        help_text=_("Product in cart"),
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cart_items",
        help_text=_("Product variant (size/color)"),
    )
    quantity = models.PositiveIntegerField(
        _("quantity"),
        default=1,
        validators=[MinValueValidator(1)],
        help_text=_("Quantity of this item"),
    )

    class Meta:
        verbose_name = _("cart item")
        verbose_name_plural = _("cart items")
        ordering = ["-created_at"]
        unique_together = [["cart", "product", "variant"]]
        indexes = [
            models.Index(fields=["cart", "product"]),
        ]

    def __str__(self):
        """Return string representation of the cart item."""
        variant_info = f" ({self.variant})" if self.variant else ""
        return f"{self.quantity}x {self.product.name}{variant_info}"

    @property
    def price(self):
        """Get price per unit."""
        if self.variant:
            return self.variant.final_price
        return self.product.price

    @property
    def total_price(self):
        """Calculate total price for this item."""
        return self.price * self.quantity

    def increase_quantity(self, amount=1):
        """Increase item quantity."""
        self.quantity += amount
        self.save(update_fields=["quantity"])

    def decrease_quantity(self, amount=1):
        """Decrease item quantity."""
        if self.quantity > amount:
            self.quantity -= amount
            self.save(update_fields=["quantity"])
        else:
            self.delete()
