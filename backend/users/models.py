from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_username


class User(AbstractUser):
    """Информация о пользователях."""

    USER = "user"
    ADMIN = "admin"
    ROLES = (
        (USER, "Аутентифицированный пользователь"),
        (ADMIN, "Администратор"),
    )

    email = models.EmailField(
        "Адрес электронной почты", unique=True, max_length=254)
    username = models.CharField(
        "Имя на сайте",
        max_length=150,
        unique=True,
        validators=(validate_username,)
    )
    first_name = models.CharField("Имя", max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)
    password = models.TextField("Пароль", max_length=150)
    role = models.CharField("Роль", max_length=250,
                            choices=ROLES, default=USER)

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """Информация о подписках."""

    user = models.ForeignKey(
        User,
        related_name="subscriber",
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name="subscribing",
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Подписки"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.username} подписан на {self.author.username}"
