from django.apps import AppConfig


class PaymentConfig(AppConfig):
    """Configuration class for the payment application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.payment"
    verbose_name = "Payment"