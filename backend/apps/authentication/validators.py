import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number_format(value):
    cleaned_value = re.sub(r'[\s\-\(\)]', '', value)
    phone_regex = re.compile(r'^\+?\d{9,15}$')
    if not phone_regex.match(cleaned_value):
        raise ValidationError(
            _(
                'Phone number must be entered in the format: "+999999999". '
                'Up to 15 digits allowed.'
            )
        )
