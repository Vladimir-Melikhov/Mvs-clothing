from django.db import models
from django.db.models import QuerySet


class SoftDeleteQuerySet(QuerySet):
    """Custom QuerySet that excludes soft-deleted objects by default."""

    def delete(self):
        """Soft delete all objects in the queryset."""
        from django.utils import timezone

        return self.update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        """Permanently delete all objects in the queryset."""
        return super().delete()

    def alive(self):
        """Return only non-deleted objects."""
        return self.filter(is_deleted=False)

    def dead(self):
        """Return only soft-deleted objects."""
        return self.filter(is_deleted=True)

    def restore(self):
        """Restore all soft-deleted objects in the queryset."""
        return self.update(is_deleted=False, deleted_at=None)


class SoftDeleteManager(models.Manager):
    """
    Custom manager that automatically excludes soft-deleted objects.
    """

    def get_queryset(self):
        """Return queryset excluding soft-deleted objects."""
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def all_with_deleted(self):
        """Return all objects including soft-deleted ones."""
        return SoftDeleteQuerySet(self.model, using=self._db)

    def deleted_only(self):
        """Return only soft-deleted objects."""
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=True)
