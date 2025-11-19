from django.contrib import admin
from django.utils.html import format_html
from decimal import Decimal
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items."""

    model = OrderItem
    extra = 0
    readonly_fields = ["price_display", "total_price_display"]
    fields = ["product", "variant", "quantity", "price", "price_display", "total_price_display"]

    def price_display(self, obj):
        """Display item price."""
        if obj.price is None:
            return "-"
        return f"${obj.price}"
    price_display.short_description = "Price"

    def total_price_display(self, obj):
        """Display total price."""
        if obj.price is None or obj.quantity is None:
            return "-"
        return f"${obj.total_price}"
    total_price_display.short_description = "Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""

    list_display = [
        "order_number",
        "user",
        "status_display",
        "payment_status_display",
        "total_display",
        "created_at",
    ]
    list_filter = ["status", "payment_status", "created_at"]
    search_fields = [
        "order_number",
        "user__email",
        "shipping_email",
        "shipping_first_name",
        "shipping_last_name",
    ]
    readonly_fields = ["order_number", "subtotal", "total", "created_at", "updated_at"]
    inlines = [OrderItemInline]

    fieldsets = (
        (
            "Order Information",
            {
                "fields": (
                    "order_number",
                    "user",
                    "status",
                    "payment_status",
                    "tracking_number",
                )
            },
        ),
        (
            "Shipping Information",
            {
                "fields": (
                    "shipping_first_name",
                    "shipping_last_name",
                    "shipping_email",
                    "shipping_phone",
                    "shipping_address",
                    "shipping_city",
                    "shipping_state",
                    "shipping_postal_code",
                    "shipping_country",
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": ("subtotal", "shipping_cost", "total"),
            },
        ),
        (
            "Additional",
            {
                "fields": ("notes",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    def status_display(self, obj):
        """Display status with color coding."""
        colors = {
            "pending": "orange",
            "processing": "blue",
            "shipped": "purple",
            "delivered": "green",
            "cancelled": "red",
        }
        color = colors.get(obj.status, "gray")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_display.short_description = "Status"

    def payment_status_display(self, obj):
        """Display payment status with color coding."""
        colors = {
            "pending": "orange",
            "paid": "green",
            "failed": "red",
            "refunded": "gray",
        }
        color = colors.get(obj.payment_status, "gray")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_payment_status_display(),
        )

    payment_status_display.short_description = "Payment"

    def total_display(self, obj):
        """Display total amount."""
        if obj.total is None:
            return "-"
        return f"${obj.total}"

    total_display.short_description = "Total"

    def has_add_permission(self, request):
        """Disable manual order creation."""
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem model."""

    list_display = [
        "order",
        "product",
        "variant",
        "quantity",
        "price_display",
        "total_price_display",
    ]
    list_filter = ["created_at"]
    search_fields = ["order__order_number", "product__name"]
    readonly_fields = ["price", "total_price_display", "created_at", "updated_at"]

    def price_display(self, obj):
        """Display unit price."""
        if obj.price is None:
            return "-"
        return f"${obj.price}"

    price_display.short_description = "Unit Price"

    def total_price_display(self, obj):
        """Display total price."""
        if obj.price is None or obj.quantity is None:
            return "-"
        return f"${obj.total_price}"

    total_price_display.short_description = "Total"

    def has_add_permission(self, request):
        """Disable manual order item creation."""
        return False
