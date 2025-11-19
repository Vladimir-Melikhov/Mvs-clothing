import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    """
    Filter class for Product model with advanced filtering options.
    """

    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.CharFilter(field_name="category__slug")
    gender = django_filters.ChoiceFilter(choices=Product.GENDER_CHOICES)
    brand = django_filters.CharFilter(field_name="brand", lookup_expr="iexact")
    is_featured = django_filters.BooleanFilter(field_name="is_featured")
    in_stock = django_filters.BooleanFilter(
        method="filter_in_stock", label="In Stock Only"
    )

    class Meta:
        model = Product
        fields = ["category", "gender", "brand", "is_featured"]

    def filter_in_stock(self, queryset, name, value):
        """Filter products that are in stock (have variants with stock)."""
        if value:
            return queryset.filter(
                variants__is_deleted=False,
                variants__is_active=True,
                variants__stock_quantity__gt=0
            ).distinct()
        return queryset