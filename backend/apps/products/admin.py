from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductVariant


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images."""

    model = ProductImage
    extra = 1
    fields = ["image", "alt_text", "is_primary", "order"]
    classes = ["collapse"]


class ProductVariantInline(admin.TabularInline):
    """Inline admin for product variants."""

    model = ProductVariant
    extra = 1
    fields = ["size", "color", "color_hex", "sku", "stock_quantity", "price_adjustment", "is_active"]
    classes = ["collapse"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""

    list_display = ["name", "parent", "is_active", "order", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order", "name"]
    list_editable = ["order", "is_active"]

    fieldsets = (
        (None, {"fields": ("name", "slug", "description")}),
        ("Hierarchy", {"fields": ("parent",)}),
        ("Display", {"fields": ("image", "is_active", "order")}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""

    list_display = [
        "name",
        "category",
        "gender",
        "price_display",
        "total_stock",
        "is_featured",
        "is_active",
        "created_at",
    ]
    list_filter = ["category", "gender", "is_featured", "is_active", "created_at"]
    search_fields = ["name", "description", "sku", "brand"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["views_count", "total_stock", "created_at", "updated_at"]
    list_editable = ["is_featured", "is_active"]
    inlines = [ProductImageInline, ProductVariantInline]

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "description", "category", "gender", "brand")
        }),
        ("Pricing", {
            "fields": ("price", "compare_at_price")
        }),
        ("Inventory", {
            "fields": ("sku", "total_stock"),
            "description": "Stock is automatically calculated from variants"
        }),
        ("Additional", {
            "fields": ("care_instructions",),
            "classes": ("collapse",)
        }),
        ("Visibility", {
            "fields": ("is_featured", "is_active", "views_count")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def price_display(self, obj):
        """Display price with sale indicator."""
        if obj.is_on_sale:
            return format_html(
                '<span style="text-decoration: line-through;">${}</span> '
                '<span style="color: red; font-weight: bold;">${}</span>',
                obj.compare_at_price,
                obj.price
            )
        return f"${obj.price}"

    price_display.short_description = "Price"

    def total_stock(self, obj):
        """Display total stock from variants."""
        stock = obj.stock_quantity
        if stock > 0:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', stock)
        return format_html('<span style="color: red;">Out of stock</span>')
    
    total_stock.short_description = "Total Stock"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin interface for ProductImage model."""

    list_display = ["product", "image_preview", "is_primary", "order", "created_at"]
    list_filter = ["is_primary", "created_at"]
    search_fields = ["product__name", "alt_text"]
    list_editable = ["order", "is_primary"]

    def image_preview(self, obj):
        """Display image preview in admin."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Preview"


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """Admin interface for ProductVariant model."""

    list_display = [
        "product",
        "size",
        "color_display",
        "sku",
        "stock_display",
        "price_display",
        "is_active",
    ]
    list_filter = ["size", "is_active", "created_at"]
    search_fields = ["product__name", "sku", "color"]
    list_editable = ["is_active"]

    def color_display(self, obj):
        """Display color with hex preview."""
        if obj.color_hex:
            return format_html(
                '<span style="display: inline-block; width: 20px; height: 20px; '
                'background-color: {}; border: 1px solid #ccc; margin-right: 5px; '
                'vertical-align: middle;"></span> {}',
                obj.color_hex,
                obj.color
            )
        return obj.color

    color_display.short_description = "Color"

    def stock_display(self, obj):
        """Display stock with color coding."""
        if obj.stock_quantity > 10:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', obj.stock_quantity)
        elif obj.stock_quantity > 0:
            return format_html('<span style="color: orange; font-weight: bold;">{}</span>', obj.stock_quantity)
        return format_html('<span style="color: red; font-weight: bold;">Out of stock</span>')
    
    stock_display.short_description = "Stock"

    def price_display(self, obj):
        """Display final price."""
        base = obj.product.price
        adjustment = obj.price_adjustment
        final = obj.final_price
        
        if adjustment != 0:
            return format_html(
                '${} <span style="color: gray;">(${:+.2f})</span>',
                final,
                adjustment
            )
        return f"${final}"
    
    price_display.short_description = "Final Price"
