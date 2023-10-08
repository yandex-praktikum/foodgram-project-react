from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


User = get_user_model()



class MeasurementUnit(models.Model):
    name = models.CharField(max_length=200,
                            unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.ForeignKey(
        MeasurementUnit, on_delete=models.PROTECT, related_name='ingridients')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, null=True, unique=True)
    slug = models.SlugField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)])
    tags = models.ManyToManyField(Tag, related_name='recipes')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe',
                                         related_name='recipes')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-pub_date']


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients_recipes')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredients_recipes')
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return (f'{self.recipe}: '
                f'({self.ingredient}) - {self.amount}')

    class Meta:
        ordering = ['-recipe']


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


