import logging
import stripe
from decimal import Decimal
from django.conf import settings
from django.db import transaction
from apps.core.exceptions import ValidationError, NotFoundError
from apps.orders.models import Order
from .models import Payment

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    """Service class for payment operations."""

    @staticmethod
    def create_checkout_session(order_id, user):
        """Create a Stripe Checkout session for an order."""
        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            raise NotFoundError("Order not found")

        # Check if order is already paid
        if order.payment_status == "paid":
            raise ValidationError("Order is already paid")

        # Check if payment already exists
        existing_payment = Payment.objects.filter(
            order=order, status__in=["pending", "processing"]
        ).first()

        if existing_payment and existing_payment.stripe_checkout_session_id:
            # Return existing session
            try:
                session = stripe.checkout.Session.retrieve(
                    existing_payment.stripe_checkout_session_id
                )
                if session.payment_status != "paid":
                    return existing_payment, session.url
            except stripe.error.StripeError:
                # If session expired or invalid, delete old payment and create new one
                existing_payment.delete()

        # Create line items for Stripe
        line_items = []
        for item in order.items.all():
            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(item.price * 100),  # Convert to cents
                        "product_data": {
                            "name": item.product.name,
                            "description": f"Size: {item.variant.size if item.variant else 'N/A'}, Color: {item.variant.color if item.variant else 'N/A'}",
                        },
                    },
                    "quantity": item.quantity,
                }
            )

        # Add shipping cost if any
        if order.shipping_cost > 0:
            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(order.shipping_cost * 100),
                        "product_data": {
                            "name": "Shipping",
                        },
                    },
                    "quantity": 1,
                }
            )

        try:
            # Create Stripe Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=f"{settings.FRONTEND_URL}/orders/{order.id}?payment=success",
                cancel_url=f"{settings.FRONTEND_URL}/orders/{order.id}?payment=cancelled",
                client_reference_id=str(order.id),
                customer_email=order.shipping_email,
                metadata={
                    "order_id": str(order.id),
                    "order_number": order.order_number,
                },
            )

            # Create or update payment record
            with transaction.atomic():
                # Delete any existing pending payments for this order
                Payment.objects.filter(order=order, status="pending").delete()
                
                # Create new payment
                payment = Payment.objects.create(
                    order=order,
                    stripe_payment_intent_id=checkout_session.payment_intent or f"temp_{checkout_session.id}",
                    stripe_checkout_session_id=checkout_session.id,
                    amount=order.total,
                    currency="USD",
                    status="pending",
                )

            logger.info(
                f"Created checkout session for order {order.order_number}: {checkout_session.id}"
            )

            return payment, checkout_session.url

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating checkout session: {str(e)}")
            raise ValidationError(f"Payment service error: {str(e)}")

    @staticmethod
    def handle_checkout_session_completed(session):
        """Handle successful checkout session completion."""
        try:
            order_id = session.metadata.get("order_id")
            payment_intent_id = session.payment_intent

            if not order_id:
                logger.error("No order_id in session metadata")
                return

            with transaction.atomic():
                order = Order.objects.select_for_update().get(id=order_id)
                
                # Find payment by checkout session ID
                payment = Payment.objects.select_for_update().filter(
                    order=order,
                    stripe_checkout_session_id=session.id
                ).first()
                
                if not payment:
                    logger.error(f"Payment not found for session {session.id}")
                    return

                # Update payment with actual payment_intent_id
                if payment_intent_id:
                    payment.stripe_payment_intent_id = payment_intent_id
                payment.status = "succeeded"
                payment.save(update_fields=["stripe_payment_intent_id", "status"])

                # Update order
                order.payment_status = "paid"
                order.status = "processing"
                order.save(update_fields=["payment_status", "status"])

            logger.info(f"Payment succeeded for order {order.order_number}")

        except Order.DoesNotExist:
            logger.error(f"Order not found for session {session.id}")
        except Exception as e:
            logger.error(f"Error handling checkout session: {str(e)}")

    @staticmethod
    def handle_payment_intent_failed(payment_intent):
        """Handle failed payment intent."""
        try:
            payment = Payment.objects.get(
                stripe_payment_intent_id=payment_intent.id
            )

            error_message = payment_intent.last_payment_error.get(
                "message", "Payment failed"
            ) if payment_intent.last_payment_error else "Payment failed"

            payment.mark_as_failed(error_message)

            logger.info(
                f"Payment failed for order {payment.order.order_number}: {error_message}"
            )

        except Payment.DoesNotExist:
            logger.error(f"Payment not found for intent {payment_intent.id}")

    @staticmethod
    def get_payment_by_order(order_id, user):
        """Get payment information for an order."""
        try:
            order = Order.objects.get(id=order_id, user=user)
            payment = Payment.objects.get(order=order)
            return payment
        except Order.DoesNotExist:
            raise NotFoundError("Order not found")
        except Payment.DoesNotExist:
            raise NotFoundError("Payment not found")

    @staticmethod
    def verify_webhook_signature(payload, sig_header):
        """Verify Stripe webhook signature."""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError:
            logger.error("Invalid webhook payload")
            raise ValidationError("Invalid payload")
        except stripe.error.SignatureVerificationError:
            logger.error("Invalid webhook signature")
            raise ValidationError("Invalid signature")