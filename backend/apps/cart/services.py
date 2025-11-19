import logging
from django.db import transaction
from apps.core.exceptions import NotFoundError, ValidationError
from apps.products.models import Product, ProductVariant
from .models import Cart, CartItem

logger = logging.getLogger(__name__)


class CartService:
    """Service class for cart operations."""

    @staticmethod
    def get_or_create_cart(user):
        """Get or create cart for user."""
        cart, created = Cart.objects.get_or_create(user=user)
        if created:
            logger.info(f"Created new cart for user {user.email}")
        return cart

    @staticmethod
    def get_cart(user):
        """Get user's cart with items."""
        try:
            cart = Cart.objects.prefetch_related(
                "items__product__images",
                "items__product__category",
                "items__variant",
            ).get(user=user)
            return cart
        except Cart.DoesNotExist:
            return CartService.get_or_create_cart(user)

    @staticmethod
    @transaction.atomic
    def add_to_cart(user, product_id, variant_id=None, quantity=1):
        """Add item to cart or update quantity if exists."""
        cart = CartService.get_or_create_cart(user)
        try:
            product = Product.objects.get(id=product_id, is_active=True, is_deleted=False)
        except Product.DoesNotExist:
            raise NotFoundError("Product not found")
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
                raise NotFoundError("Product variant not found")
            if not variant.is_in_stock:
                raise ValidationError("Product variant is out of stock")
            if variant.stock_quantity < quantity:
                raise ValidationError(
                    f"Only {variant.stock_quantity} items available"
                )
        else:
            if not product.is_in_stock:
                raise ValidationError("Product is out of stock")

            if product.stock_quantity < quantity:
                raise ValidationError(
                    f"Only {product.stock_quantity} items available"
                )
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={"quantity": quantity},
        )

        if not created:
            new_quantity = cart_item.quantity + quantity

            max_stock = variant.stock_quantity if variant else product.stock_quantity
            if new_quantity > max_stock:
                raise ValidationError(f"Only {max_stock} items available")

            cart_item.quantity = new_quantity
            cart_item.save(update_fields=["quantity"])

        logger.info(
            f"Added {quantity}x {product.name} to cart for {user.email}"
        )

        return cart

    @staticmethod
    @transaction.atomic
    def update_cart_item(user, item_id, quantity):
        """Update cart item quantity."""
        try:
            cart_item = CartItem.objects.select_related(
                "cart", "product", "variant"
            ).get(id=item_id, cart__user=user)
        except CartItem.DoesNotExist:
            raise NotFoundError("Cart item not found")
        if cart_item.variant:
            if quantity > cart_item.variant.stock_quantity:
                raise ValidationError(
                    f"Only {cart_item.variant.stock_quantity} items available"
                )
        else:
            if quantity > cart_item.product.stock_quantity:
                raise ValidationError(
                    f"Only {cart_item.product.stock_quantity} items available"
                )

        cart_item.quantity = quantity
        cart_item.save(update_fields=["quantity"])

        logger.info(
            f"Updated cart item {item_id} quantity to {quantity} for {user.email}"
        )

        return cart_item.cart

    @staticmethod
    @transaction.atomic
    def remove_from_cart(user, item_id):
        """Remove item from cart."""
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=user)
        except CartItem.DoesNotExist:
            raise NotFoundError("Cart item not found")

        cart = cart_item.cart
        cart_item.delete()

        logger.info(f"Removed cart item {item_id} for {user.email}")

        return cart

    @staticmethod
    @transaction.atomic
    def clear_cart(user):
        """Clear all items from cart."""
        cart = CartService.get_cart(user)
        cart.clear()

        logger.info(f"Cleared cart for {user.email}")

        return cart
