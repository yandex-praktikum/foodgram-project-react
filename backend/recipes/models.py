from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User
from foodgram.settings import COOKING_TIME
from recipes.validators import validate_hex_color


class Tag(models.Model):
    """Информациия о тегах."""
    name = models.CharField(
        verbose_name='Тег',
        max_length=100,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        validators=(validate_hex_color,),
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
    """Информациия о ингредиентах."""
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


class Recipes(models.Model):
    """Информациия о рецептах."""
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        default=1,
        validators=(
            MinValueValidator(COOKING_TIME),
            MaxValueValidator(1000),
        ),
        error_messages={'invalid': 'Время готовки от 1 до 1000 минут'}
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """Информациия об избранном."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Владелец избранного',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='in_favorite',
        verbose_name='Рецепт в избранном',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user.username}'


class ShoppingCart(models.Model):
    """Информациия о корзине рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart_user',
        verbose_name='Владелец корзины',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='in_shopping_cart',
        verbose_name='Рецепт в корзине',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'

    def __str__(self):
        return f'{self.recipe} в корзине у {self.user.username}'


class AmountIngredient(models.Model):
    """Информациия о количества ингридиеннтов для рецептов."""
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='amount_recipe',
        verbose_name='Рецепт для которого считается количество ингредиентов',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount_ingredient',
        verbose_name='Ингридиенты количество которых нужно',
    )
    amount = models.IntegerField(
        verbose_name='Количество ингридиентов',
        default=1,
        validators=(
            MinValueValidator(COOKING_TIME),
            MaxValueValidator(1000),
        ),
        error_messages={
            'invalid':
            f'Количество ингридиентов от {COOKING_TIME} до 1000 у.е.'
        }
    )

    class Meta:
        verbose_name = 'Количество ингридиентов для рецета'
        verbose_name_plural = 'Количество ингридиентов для рецепта'

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
