from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    CreateOrderView,
    CancelOrderView,
)

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("create/", CreateOrderView.as_view(), name="order-create"),
    path("<int:order_id>/", OrderDetailView.as_view(), name="order-detail"),
    path("<int:order_id>/cancel/", CancelOrderView.as_view(), name="order-cancel"),
]
