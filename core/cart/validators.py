from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_positive(value):
    if value <= 0:
        raise ValidationError(
            _(f'Ensure this value is greater than or equal to 0.'))
    return value
