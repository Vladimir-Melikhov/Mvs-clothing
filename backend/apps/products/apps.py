from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Configuration class for the products application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"
    verbose_name = "Products"

    def ready(self):
        import apps.products.signals