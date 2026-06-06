from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.core.responses import success_response, error_response
from .serializers import (
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
)
from .services import CartService


class CartView(APIView):
    """API view for retrieving and clearing cart."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get user's cart."""
        cart = CartService.get_cart(request.user)
        serializer = CartSerializer(cart)
        return success_response(
            data=serializer.data, message="Cart retrieved successfully"
        )

    def delete(self, request):
        """Clear cart."""
        cart = CartService.clear_cart(request.user)
        serializer = CartSerializer(cart)
        return success_response(
            data=serializer.data, message="Cart cleared successfully"
        )


class AddToCartView(APIView):
    """
    API view for adding items to cart.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    def post(self, request):
        """Add item to cart."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = CartService.add_to_cart(
            user=request.user,
            product_id=serializer.validated_data["product_id"],
            variant_id=serializer.validated_data.get("variant_id"),
            quantity=serializer.validated_data.get("quantity", 1),
        )

        response_serializer = CartSerializer(cart)
        return success_response(
            data=response_serializer.data,
            message="Item added to cart successfully",
            status_code=status.HTTP_201_CREATED,
        )


class CartItemView(APIView):
    """
    API view for updating and removing cart items.
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        """Update cart item quantity."""
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = CartService.update_cart_item(
            user=request.user,
            item_id=item_id,
            quantity=serializer.validated_data["quantity"],
        )

        response_serializer = CartSerializer(cart)
        return success_response(
            data=response_serializer.data,
            message="Cart item updated successfully",
        )

    def delete(self, request, item_id):
        """Remove item from cart."""
        cart = CartService.remove_from_cart(
            user=request.user, item_id=item_id
        )

        serializer = CartSerializer(cart)
        return success_response(
            data=serializer.data, message="Item removed from cart successfully"
        )
