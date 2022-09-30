from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254, unique=True, verbose_name='Электронная почта')
    username = models.CharField(
        max_length=150, unique=True, verbose_name='Имя пользователя',
        validators=[RegexValidator(regex=r'^[\w.@+-]+$',), ])
    first_name = models.CharField(
        max_length=150, verbose_name='Имя')
    last_name = models.CharField(
        max_length=150, verbose_name='Фамилия')
    password = models.CharField(
        max_length=150, verbose_name='Пароль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['id', 'username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор')
    created = models.DateTimeField(
        'Дата подписки',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription')]

    def __str__(self):
        return f'Пользователь {self.user} -> автор {self.author}'
