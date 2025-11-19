from django.db.models import Q, Prefetch
from apps.core.exceptions import NotFoundError, ValidationError
from .models import Product, ProductImage, ProductVariant, Category


class ProductService:
    """Service class for handling product business logic."""

    @staticmethod
    def get_products_queryset(filters=None):
        """
        Get optimized products queryset with filters.
        """
        queryset = Product.objects.select_related("category").prefetch_related(
            Prefetch(
                "images",
                queryset=ProductImage.objects.filter(is_deleted=False).order_by(
                    "-is_primary", "order"
                ),
            ),
            Prefetch(
                "variants",
                queryset=ProductVariant.objects.filter(is_deleted=False, is_active=True),
            ),
        ).filter(is_deleted=False, is_active=True)

        if filters:
            if filters.get("category"):
                queryset = queryset.filter(category__slug=filters["category"])
            if filters.get("gender"):
                queryset = queryset.filter(gender=filters["gender"])
            if filters.get("min_price"):
                queryset = queryset.filter(price__gte=filters["min_price"])
            if filters.get("max_price"):
                queryset = queryset.filter(price__lte=filters["max_price"])
            if filters.get("search"):
                search_term = filters["search"]
                queryset = queryset.filter(
                    Q(name__icontains=search_term)
                    | Q(description__icontains=search_term)
                    | Q(brand__icontains=search_term)
                )

            if filters.get("is_featured"):
                queryset = queryset.filter(is_featured=True)

            if filters.get("in_stock_only"):
                # Filter products that have variants with stock
                queryset = queryset.filter(
                    variants__is_deleted=False,
                    variants__is_active=True,
                    variants__stock_quantity__gt=0
                ).distinct()

            if filters.get("brand"):
                queryset = queryset.filter(brand=filters["brand"])

        return queryset

    @staticmethod
    def get_product_by_slug(slug):
        """
        Get product by slug with related data.
        """
        try:
            product = Product.objects.select_related("category").prefetch_related(
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.filter(is_deleted=False).order_by(
                        "-is_primary", "order"
                    ),
                ),
                Prefetch(
                    "variants",
                    queryset=ProductVariant.objects.filter(is_deleted=False, is_active=True),
                ),
            ).get(slug=slug, is_deleted=False, is_active=True)

            # Increment views count
            product.increment_views()

            return product
        except Product.DoesNotExist:
            raise NotFoundError("Product not found")

    @staticmethod
    def get_featured_products(limit=8):
        """
        Get featured products.
        """
        return ProductService.get_products_queryset(
            {"is_featured": True}
        )[:limit]

    @staticmethod
    def get_related_products(product, limit=4):
        """
        Get related products based on category.
        """
        return (
            ProductService.get_products_queryset()
            .filter(category=product.category)
            .exclude(id=product.id)[:limit]
        )

    @staticmethod
    def check_variant_availability(variant_id, quantity):
        """
        Check if variant is available in requested quantity.
        """
        try:
            variant = ProductVariant.objects.get(
                id=variant_id, is_deleted=False, is_active=True
            )

            if not variant.is_in_stock:
                raise ValidationError("Product variant is out of stock")

            if variant.stock_quantity < quantity:
                raise ValidationError(
                    f"Only {variant.stock_quantity} items available in stock"
                )

            return variant

        except ProductVariant.DoesNotExist:
            raise NotFoundError("Product variant not found")

    @staticmethod
    def get_product_variant(product_id, size, color):
        """
        Get specific product variant by product, size, and color.
        """
        try:
            variant = ProductVariant.objects.get(
                product_id=product_id,
                size=size,
                color=color,
                is_deleted=False,
                is_active=True,
            )
            return variant
        except ProductVariant.DoesNotExist:
            raise NotFoundError("Product variant not found")


class CategoryService:
    """
    Service class for handling category business logic.
    """

    @staticmethod
    def get_categories_tree():
        """
        Get hierarchical category tree.
        """
        root_categories = Category.objects.filter(
            parent=None, is_deleted=False, is_active=True
        ).prefetch_related("children")

        return root_categories

    @staticmethod
    def get_category_by_slug(slug):
        """
        Get category by slug.
        """
        try:
            category = Category.objects.get(
                slug=slug, is_deleted=False, is_active=True
            )
            return category
        except Category.DoesNotExist:
            raise NotFoundError("Category not found")

    @staticmethod
    def get_category_with_products(slug):
        """
        Get category with its products.
        """
        category = CategoryService.get_category_by_slug(slug)
        products = ProductService.get_products_queryset({"category": slug})
        return category, products
