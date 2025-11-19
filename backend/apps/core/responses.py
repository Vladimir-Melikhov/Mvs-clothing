from rest_framework.response import Response
from rest_framework import status
from typing import Any, Dict, Optional


def success_response(
    data: Any = None, message: str = "Success", status_code: int = status.HTTP_200_OK
) -> Response:
    """
    Return a standardized success response.
    """
    return Response(
        {"success": True, "data": data, "message": message, "errors": None},
        status=status_code,
    )


def error_response(
    message: str = "Error occurred",
    errors: Optional[Dict] = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    """
    Return a standardized error response.
    """
    return Response(
        {"success": False, "data": None, "message": message, "errors": errors or {}},
        status=status_code,
    )


def created_response(
    data: Any = None, message: str = "Resource created successfully"
) -> Response:
    """
    Return a standardized response for resource creation.
    """
    return success_response(
        data=data, message=message, status_code=status.HTTP_201_CREATED
    )


def no_content_response(message: str = "Resource deleted successfully") -> Response:
    """
    Return a standardized response for resource deletion.
    """
    return Response(
        {"success": True, "data": None, "message": message, "errors": None},
        status=status.HTTP_204_NO_CONTENT,
    )
