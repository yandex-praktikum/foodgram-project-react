from colorfield.fields import ColorField

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.constants import Limits











User = get_user_model()

class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Обозначение ингредиента',
        max_length=Limits.DESIGNATION.value
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=Limits.DESIGNATION.value
    )

    class Meta:
        ordering = ('name',)
        verbose_name = "Ингредиенты"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=("name", "measurement_unit"),
                name="unique_among_ingredient",
            ),
        ]
    def __str__(self):
        return f"{self.name}, {self.measurement_unit}."

    
class Tag(models.Model):
    name = models.CharField(
        verbose_name='Наименование тега',
        max_length=Limits.DESIGNATION.value,
        unique=True
    )
    color = ColorField(
        verbose_name='Цвет',
        default='#FF7777'
    )
    slug = models.SlugField(
        verbose_name='Ссылка',
        max_length=Limits.DESIGNATION.value,
        null=True,
        unique=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name_plural = "В какое время подавать"
        verbose_name = "в какое время подавать"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        verbose_name="В какое время подавать"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Имя поварёнка"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientRecipe",
        related_name="recipes",
        verbose_name="Ингредиенты"
    )
    name = models.CharField(
        max_length=Limits.DESIGNATION.value,
        verbose_name="Название"
    )
    image = models.ImageField(
        upload_to="recipes/images/",
        verbose_name="Вариант сервировки"
    )
    text = models.TextField(
        verbose_name="Как приготовить"
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(
            Limits.MIN_COOKING_TIME.value, 
            "Время приготовления не может быть меньше 1 минуты"
            )
        ],
        verbose_name="Время приготовления",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    
    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "рецепт"
        verbose_name_plural = "Рецепты"
        
    def __str__(self):
        return self.name

    
class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name="ingredients_recipes",
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name="ingredients_recipes",
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, 'Нельзя выбрать < 1')
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        ordering = ('-recipe',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f"{self.recipe}: " f"({self.ingredient}) - {self.amount}"

    
class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тэг для рецепта'
        verbose_name_plural = 'Тэги для рецепта'
        ordering = ('-recipe',)

    def __str__(self):
        return f"{self.tag} {self.recipe}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipe'
    )

    class Meta:
        verbose_name = "избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique user recipe"
            )
        ]
    
    def __str__(self):
        return f'{self.user} - {self.recipe.name}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique user cart'
            )
        ]
