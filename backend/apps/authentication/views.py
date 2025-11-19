from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from apps.core.responses import (success_response,
                                 error_response, created_response)
from apps.core.utils import get_client_ip
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    EmailVerificationSerializer,
)
from .services import AuthenticationService
from .permissions import IsAccountOwner


class AuthRateThrottle(AnonRateThrottle):
    rate = '5/hour'


class RegisterRateThrottle(AnonRateThrottle):
    rate = '3/hour'


class PasswordResetRateThrottle(AnonRateThrottle):
    rate = '3/hour'


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    throttle_classes = [RegisterRateThrottle]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, tokens = AuthenticationService.register_user(serializer.validated_data)

        return created_response(
            data={"user": UserSerializer(user).data, "tokens": tokens},
            message="User registered successfully. Please verify your email",
        )


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    throttle_classes = [AuthRateThrottle]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        ip_address = get_client_ip(request)
        user, tokens = AuthenticationService.login_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            ip_address=ip_address,
        )

        return success_response(
            data={"user": UserSerializer(user).data, "tokens": tokens},
            message="Login successful",
        )


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data, message="Profile retrieved successfully"
        )


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAccountOwner]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return success_response(
            data=UserSerializer(instance).data, message="Profile updated successfully"
        )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthenticationService.change_password(
            user=request.user,
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
        )

        return success_response(message="Password changed successfully")


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer
    throttle_classes = [PasswordResetRateThrottle]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthenticationService.request_password_reset(
            email=serializer.validated_data["email"]
        )

        return success_response(
            message="If an account exists with this email, a password reset link has been sent"
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthenticationService.reset_password(
            token=serializer.validated_data["token"],
            new_password=serializer.validated_data["new_password"],
        )

        return success_response(message="Password reset successfully")


class EmailVerificationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmailVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthenticationService.verify_email(token=serializer.validated_data["token"])

        return success_response(message="Email verified successfully")


class ResendVerificationEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.is_email_verified:
            return error_response(
                message="Email is already verified",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        AuthenticationService.send_verification_email(user)

        return success_response(message="Verification email sent successfully")
