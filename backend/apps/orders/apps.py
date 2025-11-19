from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """Configuration class for the orders application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.orders"
    verbose_name = "Orders"
