from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from apps.core.responses import success_response
from apps.core.pagination import CustomPageNumberPagination
from .models import Product, Category
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategorySerializer,
)
from .services import ProductService, CategoryService
from .filters import ProductFilter


@method_decorator(cache_page(60 * 15), name='dispatch')
class CategoryListView(generics.ListAPIView):
    """API view for listing categories."""

    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get_queryset(self):
        """Get all active root categories."""
        return CategoryService.get_categories_tree()

    def list(self, request, *args, **kwargs):
        """List all categories."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data, message="Categories retrieved successfully"
        )


class CategoryDetailView(generics.RetrieveAPIView):
    """
    API view for category details.
    """

    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    lookup_field = "slug"

    def get_queryset(self):
        """Get active categories."""
        return Category.objects.filter(is_deleted=False, is_active=True)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve category details."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data, message="Category retrieved successfully"
        )


class ProductListView(generics.ListAPIView):
    """API view for listing products with filtering and pagination."""

    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "brand"]
    ordering_fields = ["price", "created_at", "name", "views_count"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Get filtered products queryset."""
        return ProductService.get_products_queryset()

    def list(self, request, *args, **kwargs):
        """List products with pagination."""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data, message="Products retrieved successfully"
        )


class ProductDetailView(generics.RetrieveAPIView):
    """
    API view for product details.
    """

    permission_classes = [AllowAny]
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_object(self):
        """Get product by slug."""
        slug = self.kwargs.get("slug")
        return ProductService.get_product_by_slug(slug)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve product details."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data, message="Product retrieved successfully"
        )


# кэширование на 30 минут
@method_decorator(cache_page(60 * 30), name='dispatch')
class FeaturedProductsView(APIView):
    """
    API view for featured products.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """Get featured products."""
        limit = int(request.query_params.get("limit", 8))
        products = ProductService.get_featured_products(limit=limit)
        serializer = ProductListSerializer(
            products, many=True, context={"request": request}
        )
        return success_response(
            data=serializer.data, message="Featured products retrieved successfully"
        )


class RelatedProductsView(APIView):
    """
    API view for related products.
    """

    permission_classes = [AllowAny]

    def get(self, request, slug):
        """Get related products for a product."""
        product = ProductService.get_product_by_slug(slug)
        limit = int(request.query_params.get("limit", 4))
        related_products = ProductService.get_related_products(product, limit=limit)
        serializer = ProductListSerializer(
            related_products, many=True, context={"request": request}
        )
        return success_response(
            data=serializer.data, message="Related products retrieved successfully"
        )


class ProductSearchView(generics.ListAPIView):
    """API view for product search with autocomplete."""

    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        """Get search results."""
        query = self.request.query_params.get("q", "")
        if not query:
            return Product.objects.none()

        return ProductService.get_products_queryset({"search": query})[:10]

    def list(self, request, *args, **kwargs):
        """List search results."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data, message="Search results retrieved successfully"
        )
