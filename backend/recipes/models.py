from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .constants import (COLORS_CODE_LENGTH, INGREDIENTS_NAME_MAX_LENGTH,
                        MEASUREMENT_UNIT_NAME_MAX_LENGTH,
                        RECIPES_NAME_MAX_LENGTH, TAGS_NAME_MAX_LENGTH)

User = get_user_model()


class Follow(models.Model):
    '''Класс используется для создания подписки пользователя на
    рецепты другого пользователя.
    '''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_following'
            )
        ]


class Ingredients(models.Model):
    '''Класс Ingredients используется для описания ингредиентов
    в кулинарных рецептах
    '''
    name = models.CharField(
        'Название',
        help_text='Название ингредиента',
        max_length=INGREDIENTS_NAME_MAX_LENGTH,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        help_text='Единица измерения ингредиента',
        max_length=MEASUREMENT_UNIT_NAME_MAX_LENGTH,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_Ingredient'
            )
        ]

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}.'


class Tags(models.Model):
    '''Класс Tags используется для описания тэгов
    кулинарных рецептов
    '''
    name = models.CharField(
        'Название тэга',
        help_text='Введите название тэга',
        max_length=TAGS_NAME_MAX_LENGTH,
        unique=True,
    )
    color = models.CharField(
        'Цвет тэга',
        help_text='Введите код цвета тэга',
        max_length=COLORS_CODE_LENGTH,
        null=True,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг тэга',
        help_text='Введите слаг тэга',
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        return self.name


class Recipes(models.Model):
    '''Класс Recipes используется для описания кулинарных рецептов
    '''
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        'Название рецепта',
        help_text='Введите название рецепта',
        max_length=RECIPES_NAME_MAX_LENGTH
    )
    text = models.TextField(
        'Текстовое описание рецепта',
        help_text='Введите текст рецепта'
    )
    cooking_time = models.IntegerField(
        'Время приготовления',
        help_text='Время приготовления в минутах',
        validators=[MinValueValidator(1)]
    )
    tags = models.ManyToManyField(
        Tags,
        through='RecipeTag',
        verbose_name='Тэг рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredient',
        verbose_name='Ингредиент рецепта'
    )

    class Meta:
        default_related_name = 'recipes'
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return f'{self.author}, {self.name}.'


class RecipeTag(models.Model):
    '''Класс для связи многие-ко-многим рецептов и тэгов
    '''
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт')
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name='Тэг')

    class Meta:
        verbose_name = 'Тэг рецепта'
        verbose_name_plural = 'Тэги рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_RecipeTag'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class RecipeIngredient(models.Model):
    '''Класс для связи многие-ко-многим рецептов и ингредиентов
    '''
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент')
    amount = models.IntegerField(
        'Количество единиц ингредиента',
        help_text='Количество единиц ингредиента',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_RecipeIngredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe}, {self.ingredient}, {self.amount}'


class Favorites(models.Model):
    '''Класс используется для добавления рецепта в Избранное.
    '''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lover',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]
