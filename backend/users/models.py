from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from constants.constants import Users


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(
        'Email',
        max_length=Users.EMAIL_LEN,
        unique=True,)
    first_name = models.CharField(
        'Имя',
        max_length=Users.NAME_LEN)
    last_name = models.CharField(
        'Фамилия',
        max_length=Users.NAME_LEN)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.email
