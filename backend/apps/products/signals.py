"""
File: backend/apps/products/signals.py
Purpose: Signal handlers for product models
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductVariant


@receiver([post_save, post_delete], sender=ProductVariant)
def update_product_cache(sender, instance, **kwargs):
    """
    Clear product cache when variant changes.
    Note: stock_quantity is now a property, so no direct update needed.
    This signal can be used for cache invalidation if caching is implemented.
    """
    pass  # Stock is calculated dynamically via property