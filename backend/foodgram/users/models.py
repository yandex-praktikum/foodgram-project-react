from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField


class UserFoodgram(AbstractUser):
    USER_ROLE = 'user'
    ADMIN_ROLE = 'admin'
    CHOICES = [
        (USER_ROLE, 'Пользователь'),
        (ADMIN_ROLE, 'Администратор')
    ]
    first_name = CharField(verbose_name='Имя', max_length=150)
    last_name = CharField(verbose_name='Фамилия', max_length=150)
    password = CharField(verbose_name='Пароль', max_length=150)
    email = EmailField(
        verbose_name='Адрес электронной почты', unique=True)
    username = CharField(
        verbose_name='Имя пользователя', max_length=150, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username
