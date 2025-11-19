import logging
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.core.exceptions import NotFoundError, ValidationError
from apps.products.models import Product, ProductVariant
from .models import Order, OrderItem

logger = logging.getLogger(__name__)


class OrderService:
    """Service class for order operations."""

    @staticmethod
    def generate_order_number():
        """Generate unique order number."""
        timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
        import random

        random_num = random.randint(1000, 9999)
        return f"ORD-{timestamp}-{random_num}"

    @staticmethod
    @transaction.atomic
    def create_order(user, order_data):
        """Create a new order from validated data."""
        items_data = order_data.pop("items")
        shipping_cost = order_data.pop("shipping_cost", Decimal("0.00"))
        subtotal = Decimal("0.00")
        validated_items = []

        for item_data in items_data:
            product_id = item_data["product_id"]
            variant_id = item_data.get("variant_id")
            quantity = item_data["quantity"]
            price = Decimal(str(item_data["price"]))

            try:
                product = Product.objects.get(
                    id=product_id, is_active=True, is_deleted=False
                )
            except Product.DoesNotExist:
                raise NotFoundError(f"Product with id {product_id} not found")

            variant = None
            if variant_id:
                try:
                    variant = ProductVariant.objects.get(
                        id=variant_id,
                        product=product,
                        is_active=True,
                        is_deleted=False,
                    )
                except ProductVariant.DoesNotExist:
                    raise NotFoundError(f"Product variant with id {variant_id} not found")

                if variant.stock_quantity < quantity:
                    raise ValidationError(
                        f"Insufficient stock for {product.name} - {variant.size}/{variant.color}"
                    )
                if price != variant.final_price:
                    raise ValidationError(
                        f"Price mismatch for {product.name} - {variant.size}/{variant.color}"
                    )
            else:
                if product.stock_quantity < quantity:
                    raise ValidationError(f"Insufficient stock for {product.name}")

                if price != product.price:
                    raise ValidationError(f"Price mismatch for {product.name}")

            item_total = price * quantity
            subtotal += item_total

            validated_items.append(
                {
                    "product": product,
                    "variant": variant,
                    "quantity": quantity,
                    "price": price,
                }
            )

        total = subtotal + shipping_cost

        order = Order.objects.create(
            user=user,
            order_number=OrderService.generate_order_number(),
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total=total,
            **order_data,
        )

        for item_data in validated_items:
            OrderItem.objects.create(
                order=order,
                product=item_data["product"],
                variant=item_data["variant"],
                quantity=item_data["quantity"],
                price=item_data["price"],
            )

            # Update stock
            if item_data["variant"]:
                item_data["variant"].stock_quantity -= item_data["quantity"]
                item_data["variant"].save(update_fields=["stock_quantity"])
            else:
                # Note: Product stock is calculated from variants, so we don't update it directly
                pass

        logger.info(f"Order {order.order_number} created successfully for user {user.email}")

        return order

    @staticmethod
    def get_user_orders(user):
        """Get all orders for a user."""
        return Order.objects.filter(user=user).prefetch_related(
            "items__product__images",
            "items__product__category",
            "items__variant",
        ).order_by("-created_at")

    @staticmethod
    def get_order_by_id(user, order_id):
        """Get specific order by ID for a user."""
        try:
            order = Order.objects.prefetch_related(
                "items__product__images",
                "items__product__category",
                "items__variant",
            ).get(id=order_id, user=user)
            return order
        except Order.DoesNotExist:
            raise NotFoundError("Order not found")

    @staticmethod
    def get_order_by_number(user, order_number):
        """Get specific order by order number for a user."""
        try:
            order = Order.objects.prefetch_related(
                "items__product__images",
                "items__product__category",
                "items__variant",
            ).get(order_number=order_number, user=user)
            return order
        except Order.DoesNotExist:
            raise NotFoundError("Order not found")

    @staticmethod
    @transaction.atomic
    def cancel_order(user, order_id):
        """Cancel an order and restore stock."""
        order = OrderService.get_order_by_id(user, order_id)

        # Check if order can be cancelled
        if order.status in ["shipped", "delivered", "cancelled"]:
            raise ValidationError(
                f"Cannot cancel order with status: {order.get_status_display()}"
            )

        for item in order.items.all():
            if item.variant:
                item.variant.stock_quantity += item.quantity
                item.variant.save(update_fields=["stock_quantity"])

        order.status = "cancelled"
        order.save(update_fields=["status"])

        logger.info(f"Order {order.order_number} cancelled by user {user.email}")

        return order
