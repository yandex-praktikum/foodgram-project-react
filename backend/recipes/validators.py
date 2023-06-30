import re

from django.core.exceptions import ValidationError
from foodgram.settings import HEX_VALID


def validate_hex_color(value):
    if not re.match(HEX_VALID, value):
        raise ValidationError(
            error_messages={
                "invalid": "Введите корректный цвет в формате #RRGGBB"},
        )
