from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, PasswordResetToken, EmailVerificationToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for User model.
    """

    list_display = [
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_email_verified',
        'is_staff',
        'created_at'
    ]
    list_filter = [
        'is_active',
        'is_email_verified',
        'is_staff',
        'is_superuser',
        'created_at'
    ]
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth')
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_email_verified',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'last_login_ip', 'created_at', 'updated_at')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'is_active',
                'is_staff'
            ),
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'last_login']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Admin interface for PasswordResetToken model.
    """

    list_display = ['user', 'token', 'is_used', 'expires_at', 'created_at']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        """Disable manual creation of password reset tokens."""
        return False


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    """
    Admin interface for EmailVerificationToken model.
    """

    list_display = ['user', 'token', 'is_used', 'expires_at', 'created_at']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        """Disable manual creation of email verification tokens."""
        return False
