from django.urls import path
from .views import CartView, AddToCartView, CartItemView

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/", AddToCartView.as_view(), name="add-to-cart"),
    path("items/<int:item_id>/", CartItemView.as_view(), name="cart-item"),
]
