import re

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from ..users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=MinValueValidator(1)
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=200
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет в HEX',
        max_length=7,
        blank=True,
        null=True,
        unique=True
    )  # look for arguments to this field
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        max_length=200,
        unique=True,
        validators=RegexValidator(
            regex=re.compile(r'^[-a-zA-Z0-9_]+$'),
            message='Проверьте правильность написания слага'
        )
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    text = models.TextField(verbose_name='Описание рецепта')
    image = models.ImageField(upload_to='')  # look for arguments to this field
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=MinValueValidator(1)
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тегов',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор публикации',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        related_name='recipes',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Favourite(models.Model):
    pass


class ShoppingCart(models.Model):
    pass
