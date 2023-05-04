import re

from django.core.exceptions import ValidationError


def validate_hex_color(str):
    regex = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    p = re.compile(regex)

    if (re.search(p, str)):
        return True
    raise ValidationError(
        'Должен указываться только НЕХ цвет!'
    )
