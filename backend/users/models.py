from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator


USER_USERNAME_LEN = 150
USER_PASSWORD_LEN = 150
USER_EMAIL_LEN = 150
USER_FIRSTNAME_LEN = 150
USER_LASTNAME_LEN = 150


def username_validaor(value):
    deni_username_list = [
        'me', 'admin', 'administrator', 'moderator', 'staff',
    ]
    if value in deni_username_list:
        raise ValidationError(
            f'Подберите другое имя. {value} в списке недоступных имен'
        )


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя Пользователя',
        max_length=USER_USERNAME_LEN,
        unique=True,
        validators=[
            RegexValidator(regex=r'^[a-zA-Z0-9_.+-]+$'),
            username_validaor,
        ]
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=USER_PASSWORD_LEN,
    )
    email = models.EmailField(
        verbose_name='Электронная Почта',
        max_length=USER_EMAIL_LEN,
        unique=True,
        validators=[EmailValidator('Недопустимый email'),]
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=USER_FIRSTNAME_LEN,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=USER_LASTNAME_LEN,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self) -> str:
        return self.username
    