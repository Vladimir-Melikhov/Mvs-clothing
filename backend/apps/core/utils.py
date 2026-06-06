import hashlib
import random
import string
from typing import Any, Dict
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def generate_random_string(length: int = 32) -> str:
    """
    Generate a random alphanumeric string of specified length.
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def generate_hash(text: str) -> str:
    """
    Generate SHA256 hash of the given text.
    """
    return hashlib.sha256(text.encode()).hexdigest()


def send_email(
    subject: str,
    recipient_list: list,
    template_name: str,
    context: Dict[str, Any],
    from_email: str = None,
) -> int:
    """
    Send an email using a template.
    """
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)

    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    return send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )


def get_client_ip(request) -> str:
    """
    Extract client IP address from request.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def normalize_phone_number(phone: str) -> str:
    """
    Normalize phone number by removing non-digit characters.
    """
    return "".join(filter(str.isdigit, phone))
