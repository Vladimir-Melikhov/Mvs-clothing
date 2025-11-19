from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.core.responses import success_response, created_response
from apps.core.pagination import CustomPageNumberPagination
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer
from .services import OrderService


class OrderListView(generics.ListAPIView):
    """API view for listing user orders."""

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        """Get orders for current user."""
        return OrderService.get_user_orders(self.request.user)

    def list(self, request, *args, **kwargs):
        """List user orders with pagination."""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data, message="Orders retrieved successfully"
        )


class OrderDetailView(generics.RetrieveAPIView):
    """API view for order details."""

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_object(self):
        """Get order by ID for current user."""
        order_id = self.kwargs.get("order_id")
        return OrderService.get_order_by_id(self.request.user, order_id)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve order details."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data, message="Order retrieved successfully"
        )


class CreateOrderView(APIView):
    """API view for creating orders."""

    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer

    def post(self, request):
        """Create a new order."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService.create_order(
            user=request.user, order_data=serializer.validated_data
        )

        response_serializer = OrderSerializer(order)
        return created_response(
            data=response_serializer.data,
            message="Order created successfully",
        )


class CancelOrderView(APIView):
    """API view for cancelling orders."""

    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        """Cancel an order."""
        order = OrderService.cancel_order(user=request.user, order_id=order_id)

        serializer = OrderSerializer(order)
        return success_response(
            data=serializer.data, message="Order cancelled successfully"
        )
