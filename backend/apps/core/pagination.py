from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class that provides a consistent response format.
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Return a paginated response with standardized format.
        """
        return Response(
            OrderedDict(
                [
                    ("success", True),
                    (
                        "data",
                        OrderedDict(
                            [
                                ("count", self.page.paginator.count),
                                ("next", self.get_next_link()),
                                ("previous", self.get_previous_link()),
                                ("page_size", self.page_size),
                                ("total_pages", self.page.paginator.num_pages),
                                ("current_page", self.page.number),
                                ("results", data),
                            ]
                        ),
                    ),
                    ("message", "Data retrieved successfully"),
                    ("errors", None),
                ]
            )
        )


class LargeResultsSetPagination(PageNumberPagination):
    """Pagination class for large result sets."""

    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200


class SmallResultsSetPagination(PageNumberPagination):
    """Pagination class for small result sets."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
