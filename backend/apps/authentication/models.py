from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.core.models import TimeStampedModel
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    Custom user model that extends AbstractBaseUser.
    Uses email as the unique identifier instead of username.
    """

    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_("Required. Email address for the user account"),
    )
    first_name = models.CharField(
        _("first name"), max_length=150, blank=True, help_text=_("User first name")
    )
    last_name = models.CharField(
        _("last name"), max_length=150, blank=True, help_text=_("User last name")
    )
    phone_number = models.CharField(
        _("phone number"), max_length=20, null=True, blank=True, help_text=_("User phone number")
    )
    date_of_birth = models.DateField(
        _("date of birth"), null=True, blank=True, help_text=_("User date of birth")
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into the admin site"),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active"),
    )
    is_email_verified = models.BooleanField(
        _("email verified"),
        default=False,
        help_text=_("Designates whether the user has verified their email address"),
    )
    last_login_ip = models.GenericIPAddressField(
        _("last login IP"),
        null=True,
        blank=True,
        help_text=_("IP address of the last login"),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["is_active", "is_email_verified"]),
        ]

    def __str__(self):
        """Return string representation of the user."""
        return self.email

    def get_full_name(self):
        """
        Return the user's full name.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        """
        Return the user's short name.
        """
        return self.first_name or self.email


class PasswordResetToken(TimeStampedModel):
    """
    Model for storing password reset tokens.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
        help_text=_("User associated with this reset token"),
    )
    token = models.CharField(
        _("token"),
        max_length=255,
        unique=True,
        help_text=_("Unique token for password reset"),
    )
    is_used = models.BooleanField(
        _("is used"), default=False, help_text=_("Indicates if the token has been used")
    )
    expires_at = models.DateTimeField(
        _("expires at"), help_text=_("Token expiration date and time")
    )

    class Meta:
        verbose_name = _("password reset token")
        verbose_name_plural = _("password reset tokens")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["user", "is_used"]),
        ]

    def __str__(self):
        """Return string representation of the token."""
        return f"Reset token for {self.user.email}"

    def is_valid(self):
        """
        Check if the token is valid and not expired.
        """
        return not self.is_used and self.expires_at > timezone.now()

    def mark_as_used(self):
        """Mark the token as used."""
        self.is_used = True
        self.save(update_fields=["is_used"])


class EmailVerificationToken(TimeStampedModel):
    """
    Model for storing email verification tokens.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="email_verification_tokens",
        help_text=_("User associated with this verification token"),
    )
    token = models.CharField(
        _("token"),
        max_length=255,
        unique=True,
        help_text=_("Unique token for email verification"),
    )
    is_used = models.BooleanField(
        _("is used"), default=False, help_text=_("Indicates if the token has been used")
    )
    expires_at = models.DateTimeField(
        _("expires at"), help_text=_("Token expiration date and time")
    )

    class Meta:
        verbose_name = _("email verification token")
        verbose_name_plural = _("email verification tokens")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["user", "is_used"]),
        ]

    def __str__(self):
        """Return string representation of the token."""
        return f"Verification token for {self.user.email}"

    def is_valid(self):
        """
        Check if the token is valid and not expired.
        """
        return not self.is_used and self.expires_at > timezone.now()

    def mark_as_used(self):
        """Mark the token as used."""
        self.is_used = True
        self.save(update_fields=["is_used"])
