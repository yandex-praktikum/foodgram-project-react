from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), max_length=254, unique=True)
    password = models.CharField(_("password"), max_length=150)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)

    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    USERNAME_FIELD = "email"

    class Meta:
        ordering = ["pk"]
        verbose_name = "поварёнок"
        verbose_name_plural = "Все поварята"


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriber"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="author")

    class Meta:
        verbose_name_plural = "Подписки"
        ordering = ["author"]
        constraints = [
            models.UniqueConstraint(
                fields=["subscriber", "author"],
                name="unique subscriber author"
            )
        ]
