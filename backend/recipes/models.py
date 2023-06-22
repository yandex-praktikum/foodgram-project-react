from django.db import models
# from django.core.validators import MinValueValidator

# from users.models import User


class Tag(models.Model):
    """Модель хранения информациия о тегах"""
    name = models.CharField(
        verbose_name='Тег',
        max_length=100,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'color', 'slug'),
                name='unique_tags',
            ),
        )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Информациия о ингредиентах"""
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=200
        )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=50
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient',
            ),
        )

        def __str__(self):
            return self.name
