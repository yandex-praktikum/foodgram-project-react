from django.contrib.auth.models import AbstractUser
from django.db import models
from foodgram_backend.settings import (USER_EMAIL_MAX_LENGTH,
                                       USERNAME_MAX_LENGTH)

from users.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя, username',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        help_text='Имя пользователя',
        validators=(validate_username,),
        error_messages={
            'unique': 'Имя пользователя занято',
        },
    )
    email = models.EmailField(
        'Адрес email',
        max_length=USER_EMAIL_MAX_LENGTH,
        unique=True)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username