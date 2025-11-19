from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline admin for cart items."""

    model = CartItem
    extra = 0
    readonly_fields = ["price", "total_price"]
    fields = ["product", "variant", "quantity", "price", "total_price"]

    def price(self, obj):
        """Display item price."""
        return f"${obj.price}"

    def total_price(self, obj):
        """Display total price."""
        return f"${obj.total_price}"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for Cart model."""

    list_display = ["user", "total_items", "subtotal_display", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__email", "user__first_name", "user__last_name"]
    readonly_fields = ["total_items", "subtotal", "created_at", "updated_at"]
    inlines = [CartItemInline]

    fieldsets = (
        (None, {"fields": ("user",)}),
        (
            "Cart Summary",
            {"fields": ("total_items", "subtotal")},
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def subtotal_display(self, obj):
        """Display subtotal with currency."""
        return f"${obj.subtotal}"

    subtotal_display.short_description = "Subtotal"

    def has_add_permission(self, request):
        """Disable manual cart creation."""
        return False


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin interface for CartItem model."""

    list_display = [
        "cart",
        "product",
        "variant_display",
        "quantity",
        "price_display",
        "total_price_display",
        "created_at",
    ]
    list_filter = ["created_at"]
    search_fields = [
        "cart__user__email",
        "product__name",
        "variant__size",
        "variant__color",
    ]
    readonly_fields = ["price", "total_price", "created_at", "updated_at"]

    fieldsets = (
        (None, {"fields": ("cart", "product", "variant", "quantity")}),
        ("Pricing", {"fields": ("price", "total_price")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def variant_display(self, obj):
        """Display variant information."""
        if obj.variant:
            return format_html(
                "<span>{} / {}</span>", obj.variant.size, obj.variant.color
            )
        return "-"

    variant_display.short_description = "Variant"

    def price_display(self, obj):
        """Display unit price."""
        return f"${obj.price}"

    price_display.short_description = "Price"

    def total_price_display(self, obj):
        """Display total price."""
        return f"${obj.total_price}"

    total_price_display.short_description = "Total"

    def has_add_permission(self, request):
        """Disable manual cart item creation."""
        return False
