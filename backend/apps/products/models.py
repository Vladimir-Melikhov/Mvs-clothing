from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from apps.core.models import BaseModel


class Category(BaseModel):
    """
    Model for product categories with hierarchical structure.
    """

    name = models.CharField(
        _("name"),
        max_length=200,
        help_text=_("Category name"),
    )
    slug = models.SlugField(
        _("slug"),
        max_length=200,
        unique=True,
        help_text=_("URL-friendly category identifier"),
    )
    description = models.TextField(
        _("description"),
        blank=True,
        help_text=_("Category description"),
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        help_text=_("Parent category for hierarchical structure"),
    )
    image = models.ImageField(
        _("image"),
        upload_to="categories/%Y/%m/%d/",
        null=True,
        blank=True,
        help_text=_("Category image"),
    )
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_("Whether this category is active and visible"),
    )
    order = models.IntegerField(
        _("order"),
        default=0,
        help_text=_("Display order for sorting categories"),
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["order", "name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active", "order"]),
        ]

    def __str__(self):
        """Return string representation of the category."""
        return self.name

    def save(self, *args, **kwargs):
        """Override save to auto-generate slug from name."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_all_children(self):
        """Get all child categories recursively."""
        children = list(self.children.filter(is_deleted=False))
        for child in list(children):
            children.extend(child.get_all_children())
        return children


class Product(BaseModel):
    """
    Main product model containing core product information.
    """

    GENDER_CHOICES = [
        ("men", _("Men")),
        ("women", _("Women")),
        ("unisex", _("Unisex")),
    ]

    name = models.CharField(
        _("name"),
        max_length=255,
        help_text=_("Product name"),
    )
    slug = models.SlugField(
        _("slug"),
        max_length=255,
        unique=True,
        help_text=_("URL-friendly product identifier"),
    )
    description = models.TextField(
        _("description"),
        help_text=_("Detailed product description"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        help_text=_("Product category"),
    )
    gender = models.CharField(
        _("gender"),
        max_length=10,
        choices=GENDER_CHOICES,
        help_text=_("Target gender for the product"),
    )
    price = models.DecimalField(
        _("price"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Product base price"),
    )
    compare_at_price = models.DecimalField(
        _("compare at price"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Original price for showing discounts"),
    )
    sku = models.CharField(
        _("SKU"),
        max_length=100,
        unique=True,
        help_text=_("Stock Keeping Unit"),
    )
    brand = models.CharField(
        _("brand"),
        max_length=100,
        blank=True,
        help_text=_("Product brand"),
    )
    care_instructions = models.TextField(
        _("care instructions"),
        blank=True,
        help_text=_("Product care and maintenance instructions"),
    )
    is_featured = models.BooleanField(
        _("is featured"),
        default=False,
        help_text=_("Whether this product is featured on homepage"),
    )
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_("Whether this product is active and visible"),
    )
    views_count = models.IntegerField(
        _("views count"),
        default=0,
        help_text=_("Number of times product was viewed"),
    )

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["category", "is_active"]),
            models.Index(fields=["gender", "is_active"]),
            models.Index(fields=["is_featured", "is_active"]),
            models.Index(fields=["sku"]),
        ]

    def __str__(self):
        """Return string representation of the product."""
        return self.name

    def save(self, *args, **kwargs):
        """Override save to auto-generate slug from name."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_on_sale(self):
        """Check if product is on sale."""
        return (
            self.compare_at_price
            and self.compare_at_price > self.price
        )

    @property
    def discount_percentage(self):
        """Calculate discount percentage."""
        if not self.is_on_sale:
            return 0
        return int(
            ((self.compare_at_price - self.price) / self.compare_at_price) * 100
        )

    @property
    def stock_quantity(self):
        """Get total stock from all variants."""
        return sum(
            self.variants.filter(is_deleted=False, is_active=True)
            .values_list("stock_quantity", flat=True)
        )

    @property
    def is_in_stock(self):
        """Check if product is in stock."""
        return self.stock_quantity > 0

    def increment_views(self):
        """Increment product views count."""
        self.views_count += 1
        self.save(update_fields=["views_count"])


class ProductImage(BaseModel):
    """
    Model for storing multiple images per product.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        help_text=_("Associated product"),
    )
    image = models.ImageField(
        _("image"),
        upload_to="products/%Y/%m/%d/",
        help_text=_("Product image"),
    )
    alt_text = models.CharField(
        _("alt text"),
        max_length=255,
        blank=True,
        help_text=_("Alternative text for accessibility"),
    )
    is_primary = models.BooleanField(
        _("is primary"),
        default=False,
        help_text=_("Whether this is the primary product image"),
    )
    order = models.IntegerField(
        _("order"),
        default=0,
        help_text=_("Display order for sorting images"),
    )

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")
        ordering = ["order", "-is_primary"]
        indexes = [
            models.Index(fields=["product", "is_primary"]),
        ]

    def __str__(self):
        """Return string representation of the product image."""
        return f"{self.product.name} - Image {self.order}"

    def save(self, *args, **kwargs):
        """Override save to ensure only one primary image per product."""
        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product, is_primary=True
            ).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductVariant(BaseModel):
    """
    Model for product variants (size, color combinations).
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
        help_text=_("Associated product"),
    )
    size = models.CharField(
        _("size"),
        max_length=20,
        help_text=_("Product size (XS, S, M, L, XL, etc.)"),
    )
    color = models.CharField(
        _("color"),
        max_length=50,
        help_text=_("Product color"),
    )
    color_hex = models.CharField(
        _("color hex code"),
        max_length=7,
        blank=True,
        help_text=_("Hexadecimal color code"),
    )
    sku = models.CharField(
        _("SKU"),
        max_length=100,
        unique=True,
        help_text=_("Variant-specific SKU"),
    )
    stock_quantity = models.IntegerField(
        _("stock quantity"),
        default=0,
        help_text=_("Available stock for this variant"),
    )
    price_adjustment = models.DecimalField(
        _("price adjustment"),
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text=_("Price adjustment for this variant (can be negative)"),
    )
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_("Whether this variant is active"),
    )

    class Meta:
        verbose_name = _("product variant")
        verbose_name_plural = _("product variants")
        ordering = ["size", "color"]
        unique_together = [["product", "size", "color"]]
        indexes = [
            models.Index(fields=["product", "is_active"]),
            models.Index(fields=["sku"]),
        ]

    def __str__(self):
        """Return string representation of the variant."""
        return f"{self.product.name} - {self.size} / {self.color}"

    @property
    def final_price(self):
        """Calculate final price including adjustment."""
        return self.product.price + self.price_adjustment

    @property
    def is_in_stock(self):
        """Check if variant is in stock."""
        return self.stock_quantity > 0