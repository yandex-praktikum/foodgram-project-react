from django.core.validators import MinValueValidator
from django.db import models
from ..users.models import User


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
        unique=True
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
    tags = models.ForeignKey(
        Tag,
        verbose_name='Список тегов',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE
    )
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name='Список ингредиентов',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Favourite(models.Model):
    pass


class ShoppingCart(models.Model):
    pass
