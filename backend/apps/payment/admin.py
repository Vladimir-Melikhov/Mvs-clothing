from django.contrib import admin
from django.utils.html import format_html
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for Payment model."""

    list_display = [
        "order",
        "amount_display",
        "status_display",
        "payment_method",
        "created_at",
    ]
    list_filter = ["status", "currency", "created_at"]
    search_fields = [
        "order__order_number",
        "stripe_payment_intent_id",
        "stripe_checkout_session_id",
    ]
    readonly_fields = [
        "order",
        "stripe_payment_intent_id",
        "stripe_checkout_session_id",
        "amount",
        "currency",
        "status",
        "payment_method",
        "receipt_url",
        "error_message",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Order Information",
            {
                "fields": ("order",)
            },
        ),
        (
            "Stripe Information",
            {
                "fields": (
                    "stripe_payment_intent_id",
                    "stripe_checkout_session_id",
                    "payment_method",
                    "receipt_url",
                )
            },
        ),
        (
            "Payment Details",
            {
                "fields": ("amount", "currency", "status", "error_message")
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at")
            },
        ),
    )

    def amount_display(self, obj):
        """Display amount with currency."""
        return f"${obj.amount} {obj.currency}"

    amount_display.short_description = "Amount"

    def status_display(self, obj):
        """Display status with color coding."""
        colors = {
            "pending": "orange",
            "processing": "blue",
            "succeeded": "green",
            "failed": "red",
            "cancelled": "gray",
            "refunded": "purple",
        }
        color = colors.get(obj.status, "gray")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_display.short_description = "Status"

    def has_add_permission(self, request):
        """Disable manual payment creation."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable payment deletion."""
        return False
