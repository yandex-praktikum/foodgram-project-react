from django.db.models import CharField, EmailField
from django.contrib.auth.models import AbstractUser


class UserFoodgram(AbstractUser):
    USER_ROLE = 'user'
    ADMIN_ROLE = 'admin'
    CHOICES = [
        (USER_ROLE, 'Пользователь'),
        (ADMIN_ROLE, 'Администратор')
    ]
    email = EmailField(unique=True)
    username = CharField(max_length=150, unique=True)
    password = CharField(verbose_name='Пароль', max_length=150)
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
