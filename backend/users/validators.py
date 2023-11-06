import re
from django.core.validators import ValidationError

def validate_name(value):
    # Проверяем, что значение не пустое
    if not value:
        raise ValidationError('Имя не может быть пустым')



    # Проверяем, что все символы в имени принадлежат одному языку
    lang = ''
    for char in value:
        # Определяем язык символа с помощью его кода
        char_lang = 'latin' if ord(char) < 128 else 'non-latin'

        # Если это первый символ, устанавливаем язык
        if not lang:
            lang = char_lang
        # Если текущий символ отличается от предыдущего языка, вызываем исключение
        elif char_lang != lang:
            raise ValidationError('Имя должно быть на одном языке')

    # Если все проверки пройдены успешно, возвращаем значение
    return value