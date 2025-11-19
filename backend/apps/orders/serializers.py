from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items."""

    product = ProductListSerializer(read_only=True)
    variant_details = serializers.SerializerMethodField()
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "variant_details",
            "quantity",
            "price",
            "total_price",
            "created_at",
        ]
        read_only_fields = ["id", "price", "created_at"]

    def get_variant_details(self, obj):
        """Get variant details if exists."""
        if obj.variant:
            return {
                "id": obj.variant.id,
                "size": obj.variant.size,
                "color": obj.variant.color,
                "color_hex": obj.variant.color_hex,
            }
        return None


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order list and detail."""

    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    payment_status_display = serializers.CharField(
        source="get_payment_status_display", read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "status_display",
            "payment_status",
            "payment_status_display",
            "shipping_first_name",
            "shipping_last_name",
            "shipping_email",
            "shipping_phone",
            "shipping_address",
            "shipping_city",
            "shipping_state",
            "shipping_postal_code",
            "shipping_country",
            "subtotal",
            "shipping_cost",
            "total",
            "notes",
            "tracking_number",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "order_number",
            "subtotal",
            "total",
            "created_at",
            "updated_at",
        ]


class CreateOrderItemSerializer(serializers.Serializer):
    """Serializer for creating order items."""

    product_id = serializers.IntegerField(required=True)
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1, required=True)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=True, min_value=0
    )


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating orders."""

    shipping_first_name = serializers.CharField(max_length=150, required=True)
    shipping_last_name = serializers.CharField(max_length=150, required=True)
    shipping_email = serializers.EmailField(required=True)
    shipping_phone = serializers.CharField(max_length=20, required=True)
    shipping_address = serializers.CharField(max_length=255, required=True)
    shipping_city = serializers.CharField(max_length=100, required=True)
    shipping_state = serializers.CharField(max_length=100, required=True)
    shipping_postal_code = serializers.CharField(max_length=20, required=True)
    shipping_country = serializers.CharField(max_length=100, required=True)

    items = CreateOrderItemSerializer(many=True, required=True)

    notes = serializers.CharField(required=False, allow_blank=True)
    shipping_cost = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, default=0
    )

    def validate_items(self, value):
        """Validate that items list is not empty."""
        if not value:
            raise serializers.ValidationError("Order must contain at least one item")
        return value
