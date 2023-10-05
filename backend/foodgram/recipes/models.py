from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200, unique=True)
    

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    cooking_time = models.PositiveIntegerField() # валидац на мин
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(
        'Ingredient', 
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'))
    

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_ingredients', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='recipe_ingredients', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            )
        ]
    def __str__(self):
        return f'{self.ingredient.name} - {self.amount}'
