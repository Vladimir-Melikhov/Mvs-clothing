import logging
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from django.db import transaction
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from apps.core.utils import generate_random_string, send_email
from apps.core.exceptions import AuthenticationError, ValidationError, NotFoundError
from .models import User, PasswordResetToken, EmailVerificationToken

logger = logging.getLogger(__name__)


class AuthenticationService:

    @staticmethod
    def register_user(validated_data):
        with transaction.atomic():
            data = validated_data.copy()
            password = data.pop("password")
            data.pop("password_confirm", None)
            user = User.objects.create_user(password=password, **data)
            tokens = AuthenticationService.generate_tokens(user)
            AuthenticationService.send_verification_email(user)

            logger.info(f"New user registered: {user.email}")

        return user, tokens

    @staticmethod
    def login_user(email, password, ip_address=None):
        try:
            user = authenticate(email=email, password=password)

            if user is None:
                logger.warning(f"Failed login attempt for {email} from {ip_address}")
                raise AuthenticationError("Invalid email or password")

            if not user.is_active:
                logger.warning(f"Login attempt for inactive account: {email} from {ip_address}")
                raise AuthenticationError("Account is deactivated")

            if ip_address:
                user.last_login_ip = ip_address
                user.save(update_fields=["last_login_ip", "last_login"])

            tokens = AuthenticationService.generate_tokens(user)

            logger.info(f"Successful login: {email} from {ip_address}")

            return user, tokens
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Login error for {email}: {str(e)}")
            raise

    @staticmethod
    def generate_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @staticmethod
    def change_password(user, old_password, new_password):
        if not user.check_password(old_password):
            logger.warning(f"Failed password change attempt for {user.email}: incorrect old password")
            raise ValidationError("Current password is incorrect")

        user.set_password(new_password)
        user.save(update_fields=["password"])

        logger.info(f"Password changed successfully for {user.email}")

    @staticmethod
    def request_password_reset(email):
        try:
            user = User.objects.get(email__iexact=email, is_active=True)
        except User.DoesNotExist:
            logger.info(f"Password reset requested for non-existent email: {email}")
            return

        token = generate_random_string(64)
        expires_at = timezone.now() + timedelta(hours=24)

        PasswordResetToken.objects.create(user=user, token=token, expires_at=expires_at)

        AuthenticationService.send_password_reset_email(user, token)

        logger.info(f"Password reset token generated for {user.email}")

    @staticmethod
    def reset_password(token, new_password):
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            logger.warning(f"Invalid password reset token attempted: {token[:10]}...")
            raise NotFoundError("Invalid or expired reset token")

        if not reset_token.is_valid():
            logger.warning(f"Expired password reset token used for {reset_token.user.email}")
            raise ValidationError("Token has expired or already been used")

        user = reset_token.user
        user.set_password(new_password)
        user.save(update_fields=["password"])

        reset_token.mark_as_used()

        logger.info(f"Password reset successfully for {user.email}")

    @staticmethod
    def send_verification_email(user):
        token = generate_random_string(64)
        expires_at = timezone.now() + timedelta(days=7)

        EmailVerificationToken.objects.create(
            user=user, token=token, expires_at=expires_at
        )

        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
        verification_url = f"{frontend_url}/email/verify?token={token}"

        send_email(
            subject='Verify your email address',
            recipient_list=[user.email],
            template_name='authentication/email_verification.html',
            context={'user': user, 'token': token, 'verification_url': verification_url}
        )

        logger.info(f"Verification email sent to {user.email}")

    @staticmethod
    def verify_email(token):
        try:
            verification_token = EmailVerificationToken.objects.get(token=token)
        except EmailVerificationToken.DoesNotExist:
            logger.warning(f"Invalid email verification token attempted: {token[:10]}...")
            raise NotFoundError("Invalid or expired verification token")

        if not verification_token.is_valid():
            logger.warning(f"Expired verification token used for {verification_token.user.email}")
            raise ValidationError("Token has expired or already been used")

        user = verification_token.user
        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        verification_token.mark_as_used()

        logger.info(f"Email verified successfully for {user.email}")

    @staticmethod
    def send_password_reset_email(user, token):
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
        reset_url = f"{frontend_url}/password-reset/confirm?token={token}"

        send_email(
            subject='Reset your password',
            recipient_list=[user.email],
            template_name='authentication/password_reset.html',
            context={'user': user, 'token': token, 'reset_url': reset_url}
        )

        logger.info(f"Password reset email sent to {user.email}")
