import re

from django.core.exceptions import ValidationError

REGEX_USERNAME = re.compile(r'^[\w.@+-]+')


def validate_username(name):
    """Валидация имени пользователя."""
    if not REGEX_USERNAME.fullmatch(name):
        raise ValidationError(
            'Для имени доступны буквы A - Z,  a - z и символы _.+-@')
    return name
