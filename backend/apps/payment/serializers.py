from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payment information."""

    order_number = serializers.CharField(source="order.order_number", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "order_number",
            "stripe_payment_intent_id",
            "stripe_checkout_session_id",
            "amount",
            "currency",
            "status",
            "status_display",
            "payment_method",
            "receipt_url",
            "error_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
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


class CreateCheckoutSessionSerializer(serializers.Serializer):
    """Serializer for creating a checkout session."""

    order_id = serializers.IntegerField(required=True)

    def validate_order_id(self, value):
        """Validate that order exists and belongs to user."""
        from apps.orders.models import Order

        try:
            order = Order.objects.get(id=value)
            request = self.context.get("request")

            if request and order.user != request.user:
                raise serializers.ValidationError("Order does not belong to you")

            if order.payment_status == "paid":
                raise serializers.ValidationError("Order is already paid")

            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found")
