import re

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True
    )  # unique or not?
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        validators=RegexValidator(
            regex=re.compile(r'^[\w.@+-]+\z'),
            message='Проверьте правильность написания никнейма'
        )
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=150
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150
    )

    def __str__(self):
        return self.username


class Subscription(models.Model):
    pass
