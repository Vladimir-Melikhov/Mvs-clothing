from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import SoftDeleteManager


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    'created_at' and 'updated_at' fields.
    """

    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("Date and time when the object was created"),
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        help_text=_("Date and time when the object was last updated"),
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SoftDeleteModel(models.Model):
    """
    Abstract base model that provides soft delete functionality.
    Objects are not actually deleted from the database, but marked as deleted.
    """

    is_deleted = models.BooleanField(
        _("is deleted"),
        default=False,
        help_text=_("Indicates if the object has been soft deleted"),
    )
    deleted_at = models.DateTimeField(
        _("deleted at"),
        null=True,
        blank=True,
        help_text=_("Date and time when the object was soft deleted"),
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, hard=False):
        """
        Soft delete the object by default. Use hard=True for permanent deletion.
        """
        if hard:
            super().delete(using=using, keep_parents=keep_parents)
        else:
            from django.utils import timezone

            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        """Restore a soft-deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])


class BaseModel(TimeStampedModel, SoftDeleteModel):
    """
    Base model that combines timestamped and soft delete functionality.
    All application models should inherit from this class.
    """

    class Meta:
        abstract = True
