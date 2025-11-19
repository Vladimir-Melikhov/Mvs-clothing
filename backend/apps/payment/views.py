import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from apps.core.responses import success_response, error_response, created_response
from .serializers import PaymentSerializer, CreateCheckoutSessionSerializer
from .services import PaymentService

logger = logging.getLogger(__name__)


class CreateCheckoutSessionView(APIView):
    """API view for creating Stripe checkout session."""

    permission_classes = [IsAuthenticated]
    serializer_class = CreateCheckoutSessionSerializer

    def post(self, request):
        """Create a Stripe checkout session."""
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data["order_id"]

        payment, checkout_url = PaymentService.create_checkout_session(
            order_id=order_id, user=request.user
        )

        return created_response(
            data={
                "payment": PaymentSerializer(payment).data,
                "checkout_url": checkout_url,
            },
            message="Checkout session created successfully",
        )


class PaymentDetailView(APIView):
    """API view for retrieving payment details."""

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        """Get payment details for an order."""
        payment = PaymentService.get_payment_by_order(
            order_id=order_id, user=request.user
        )

        serializer = PaymentSerializer(payment)
        return success_response(
            data=serializer.data, message="Payment details retrieved successfully"
        )


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):
    """API view for handling Stripe webhooks."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle Stripe webhook events."""
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        if not sig_header:
            logger.error("No Stripe signature in request")
            return HttpResponse(status=400)

        try:
            event = PaymentService.verify_webhook_signature(payload, sig_header)
        except Exception as e:
            logger.error(f"Webhook verification failed: {str(e)}")
            return HttpResponse(status=400)

        # Handle the event
        event_type = event["type"]
        event_data = event["data"]["object"]

        logger.info(f"Received webhook event: {event_type}")

        if event_type == "checkout.session.completed":
            PaymentService.handle_checkout_session_completed(event_data)
        elif event_type == "payment_intent.succeeded":
            logger.info(f"Payment intent succeeded: {event_data.get('id')}")
        elif event_type == "payment_intent.payment_failed":
            PaymentService.handle_payment_intent_failed(event_data)
        else:
            logger.info(f"Unhandled event type: {event_type}")

        return HttpResponse(status=200)
