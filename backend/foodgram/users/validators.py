from django.core.exceptions import ValidationError


def validate_username(value):
    """Валидатор имени пользователя."""
    if value == 'me':
        return ValidationError('Недопустимое имя пользователя.')
    return value
