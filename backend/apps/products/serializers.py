"""
File: backend/apps/products/serializers.py
Purpose: Serializers for product models
"""

from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    children_count = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "parent",
            "image",
            "is_active",
            "order",
            "children_count",
            "products_count",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_children_count(self, obj):
        """Get count of child categories."""
        return obj.children.filter(is_deleted=False, is_active=True).count()

    def get_products_count(self, obj):
        """Get count of products in category."""
        return obj.products.filter(is_deleted=False, is_active=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for ProductImage model."""
    
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "alt_text",
            "is_primary",
            "order",
        ]
        read_only_fields = ["id"]
    
    def get_image(self, obj):
        """Get absolute URL for image."""
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return None


class ProductVariantSerializer(serializers.ModelSerializer):
    """Serializer for ProductVariant model."""

    final_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "size",
            "color",
            "color_hex",
            "sku",
            "stock_quantity",
            "price_adjustment",
            "final_price",
            "is_in_stock",
            "is_active",
        ]
        read_only_fields = ["id"]


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product list view."""

    category_name = serializers.CharField(source="category.name", read_only=True)
    primary_image = serializers.SerializerMethodField()
    is_on_sale = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    stock_quantity = serializers.IntegerField(read_only=True)  # This is now a property

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category_name",
            "gender",
            "price",
            "compare_at_price",
            "is_on_sale",
            "discount_percentage",
            "primary_image",
            "is_featured",
            "is_in_stock",
            "stock_quantity",
            "brand",
        ]

    def get_primary_image(self, obj):
        """Get primary product image with absolute URL."""
        request = self.context.get("request")
        
        # Try to get primary image first
        primary_image = obj.images.filter(is_primary=True, is_deleted=False).first()
        
        # If no primary image, get the first available image
        if not primary_image:
            primary_image = obj.images.filter(is_deleted=False).order_by('order', 'id').first()
        
        if primary_image and primary_image.image:
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for product detail view."""

    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    is_on_sale = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    stock_quantity = serializers.IntegerField(read_only=True)  # This is now a property
    available_sizes = serializers.SerializerMethodField()
    available_colors = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "category",
            "gender",
            "price",
            "compare_at_price",
            "is_on_sale",
            "discount_percentage",
            "sku",
            "brand",
            "care_instructions",
            "is_featured",
            "is_in_stock",
            "stock_quantity",
            "views_count",
            "images",
            "variants",
            "available_sizes",
            "available_colors",
            "created_at",
            "updated_at",
        ]

    def get_available_sizes(self, obj):
        """Get list of available sizes."""
        return list(
            obj.variants.filter(is_deleted=False, is_active=True, stock_quantity__gt=0)
            .values_list("size", flat=True)
            .distinct()
        )

    def get_available_colors(self, obj):
        """Get list of available colors."""
        colors = obj.variants.filter(
            is_deleted=False, is_active=True, stock_quantity__gt=0
        ).values("color", "color_hex").distinct()
        return list(colors)
