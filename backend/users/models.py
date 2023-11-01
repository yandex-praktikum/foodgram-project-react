from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserFoodgram(AbstractUser):
    '''Модель фудграм юзера'''
    email = models.EmailField(
        max_length=254,
        help_text='введите е-mail',
        verbose_name='электронная почта',
        unique=True
    )
    username = models.CharField(
        max_length=150,
        verbose_name='имя пользователя',
        help_text='введите Ваш псевдоним',
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='введите Ваше имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='введите Вашу фамилию',
    )
    password = models.CharField(
        verbose_name=_("Пароль"),  # так _ в родителе, хз зачем, люди делают так же. РАЗОБРАТЬСЯ!!
        max_length=150,
        help_text="Максимум 128 символов",
    )

    class Meta:
        '''Метамодель для модели UserFoodgram'''
        ordering = ['username',]
        verbose_name = 'пользователь',
        verbose_name_plural = 'пользователи'

        def __str__(self):
            return self.username
