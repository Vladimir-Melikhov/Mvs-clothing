from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error responses.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            "success": False,
            "data": None,
            "message": "",
            "errors": {},
        }

        if isinstance(response.data, dict):
            if "detail" in response.data:
                custom_response_data["message"] = response.data["detail"]
            else:
                custom_response_data["errors"] = response.data
                custom_response_data["message"] = "Validation error occurred"
        elif isinstance(response.data, list):
            custom_response_data["message"] = (
                response.data[0] if response.data else "An error occurred"
            )
        else:
            custom_response_data["message"] = str(response.data)

        response.data = custom_response_data

    return response


class BaseAPIException(APIException):
    """Base exception class for API exceptions."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("An error occurred")
    default_code = "error"


class ValidationError(BaseAPIException):
    """Exception raised when validation fails."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid input data")
    default_code = "validation_error"


class NotFoundError(BaseAPIException):
    """Exception raised when a resource is not found."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("Resource not found")
    default_code = "not_found"


class PermissionDeniedError(BaseAPIException):
    """Exception raised when permission is denied."""

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("Permission denied")
    default_code = "permission_denied"


class AuthenticationError(BaseAPIException):
    """Exception raised when authentication fails."""

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Authentication failed")
    default_code = "authentication_error"


class ConflictError(BaseAPIException):
    """Exception raised when there is a conflict."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = _("Conflict occurred")
    default_code = "conflict_error"


class ServiceUnavailableError(BaseAPIException):
    """Exception raised when a service is unavailable."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = _("Service temporarily unavailable")
    default_code = "service_unavailable"
