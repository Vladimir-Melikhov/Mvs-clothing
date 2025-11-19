from django.urls import path
from .views import CreateCheckoutSessionView, PaymentDetailView, StripeWebhookView

app_name = "payment"

urlpatterns = [
    path(
        "create-checkout-session/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path(
        "order/<int:order_id>/",
        PaymentDetailView.as_view(),
        name="payment-detail",
    ),
    path("webhook/", StripeWebhookView.as_view(), name="stripe-webhook"),
]
