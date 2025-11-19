from django.apps import AppConfig


class CartConfig(AppConfig):
    """Configuration class for the cart application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.cart"
    verbose_name = "Cart"