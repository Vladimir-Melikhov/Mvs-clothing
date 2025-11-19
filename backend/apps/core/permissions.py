from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission class that allows access only to object owners.
    """

    message = "You do not have permission to access this resource"

    def has_object_permission(self, request, view, obj):
        """
        Check if the user owns the object.
        """
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission class that allows read-only access to everyone
    and write access only to owners.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check object-level permissions.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission class that allows read-only access to everyone
    and write access only to admin users.
    """

    def has_permission(self, request, view):
        """
        Check view-level permissions.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff
