from django.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator,)

TAG_NAME_LEN = 200
TAG_SLUG_LEN = 100
INGRIDIENT_NAME_LEN = 200
AUTHOR_NAME_LEN = 200
RECIPE_NAME_LEN = 200

class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=TAG_NAME_LEN,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цыетовой код',
        max_length=54,
        unique=True,
        validators=[RegexValidator(regex='#[a-fA-F0-9]{6}'),]

    )
    slug = models.CharField(
        verbose_name='Slug',
        max_length=TAG_SLUG_LEN,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=INGRIDIENT_NAME_LEN,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=54,
    )


class Recipe(models.Model):
    author = models.CharField(
        verbose_name='Автор',
        max_length=AUTHOR_NAME_LEN
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=RECIPE_NAME_LEN
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/'
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
        max_length=2000,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='продукты для приготовления',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
    )


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингридиенты в рецепте'
        verbose_name_plural = 'Ингридиенты в рецептах'
    
    def __str__(self) -> str:
        return f'{self.ingredient} {self.recipe}'
