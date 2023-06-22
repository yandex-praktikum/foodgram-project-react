from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram_backend.settings import (FIRST_NAME_MAX_LENGTH,
                                       LAST_NAME_MAX_LENGTH,
                                       PASSWORD_MAX_LENGTH,
                                       USER_EMAIL_MAX_LENGTH,
                                       USERNAME_MAX_LENGTH)
from users.validators import validate_username


class FoodgramUser(AbstractUser):
    username = models.CharField(
        'Логин пользователя, username',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        help_text='Введите свой логин',
        validators=(validate_username,),
        error_messages={
            'unique': 'Логин пользователя занят',
        },
    )
    email = models.EmailField(
        'Адрес email',
        help_text='Введите адрес email',
        max_length=USER_EMAIL_MAX_LENGTH,
        unique=True)

    first_name = models.CharField(
        'Имя пользователя',
        help_text='Введите своё имя',
        max_length=FIRST_NAME_MAX_LENGTH
    )

    last_name = models.CharField(
        'Фамилия пользователя',
        help_text='Введите фамилию',
        max_length=LAST_NAME_MAX_LENGTH
    )

    password = models.CharField(
        'Пароль',
        help_text='Введите пароль',
        max_length=PASSWORD_MAX_LENGTH
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
