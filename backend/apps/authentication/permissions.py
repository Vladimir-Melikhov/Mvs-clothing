from rest_framework import permissions


class IsEmailVerified(permissions.BasePermission):
    """
    Permission class that allows access only to users with verified email.
    """

    message = "Email verification is required to access this resource"

    def has_permission(self, request, view):
        """
        Check if user has verified their email.
        """
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_email_verified
        )


class IsAccountOwner(permissions.BasePermission):
    """
    Permission class that allows users to access only their own account.
    """

    message = "You can only access your own account"

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is accessing their own account.
        """
        return obj == request.user
