from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel
from apps.orders.models import Order


class Payment(TimeStampedModel):
    """Payment model for storing payment transactions."""

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("processing", _("Processing")),
        ("succeeded", _("Succeeded")),
        ("failed", _("Failed")),
        ("cancelled", _("Cancelled")),
        ("refunded", _("Refunded")),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        related_name="payment",
        help_text=_("Order associated with this payment"),
    )
    stripe_payment_intent_id = models.CharField(
        _("stripe payment intent ID"),
        max_length=255,
        unique=True,
        help_text=_("Stripe Payment Intent ID"),
    )
    stripe_checkout_session_id = models.CharField(
        _("stripe checkout session ID"),
        max_length=255,
        blank=True,
        help_text=_("Stripe Checkout Session ID"),
    )
    amount = models.DecimalField(
        _("amount"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Payment amount"),
    )
    currency = models.CharField(
        _("currency"),
        max_length=3,
        default="USD",
        help_text=_("Payment currency code"),
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text=_("Payment status"),
    )
    payment_method = models.CharField(
        _("payment method"),
        max_length=50,
        blank=True,
        help_text=_("Payment method used"),
    )
    receipt_url = models.URLField(
        _("receipt URL"),
        blank=True,
        help_text=_("URL to payment receipt"),
    )
    error_message = models.TextField(
        _("error message"),
        blank=True,
        help_text=_("Error message if payment failed"),
    )

    class Meta:
        verbose_name = _("payment")
        verbose_name_plural = _("payments")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["stripe_payment_intent_id"]),
            models.Index(fields=["order", "status"]),
        ]

    def __str__(self):
        """Return string representation of the payment."""
        return f"Payment for Order #{self.order.order_number} - {self.status}"

    def mark_as_succeeded(self):
        """Mark payment as succeeded and update order."""
        self.status = "succeeded"
        self.save(update_fields=["status"])

        # Update order payment status
        self.order.payment_status = "paid"
        self.order.status = "processing"
        self.order.save(update_fields=["payment_status", "status"])

    def mark_as_failed(self, error_message=""):
        """Mark payment as failed."""
        self.status = "failed"
        self.error_message = error_message
        self.save(update_fields=["status", "error_message"])

        # Update order payment status
        self.order.payment_status = "failed"
        self.order.save(update_fields=["payment_status"])
