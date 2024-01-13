from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import OuterRef, Exists

from core.constants import (
    MAX_STR_LENGTH,
    STR_RETURN_VALUE,
    MAXIMUM_AMOUNT_ALLOWED,
    MAX_COOKING_TIME,
    MIN_VALUE,
)
from core.models import UserRecipeBaseModel


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        'Название тега',
        max_length=MAX_STR_LENGTH,
        unique=True,
        help_text='Название тега'
    )
    color = ColorField(
        'Цвет тега',
        unique=True,
        help_text='Цвет тега',
    )
    slug = models.SlugField(
        'Слаг',
        max_length=MAX_STR_LENGTH,
        unique=True,
        help_text='Слаг',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        default_related_name = '%(class)ss'

    def __str__(self):
        return self.name[:STR_RETURN_VALUE]


class RecipeQuerySet(models.QuerySet):
    """Пользовательский кверисет для рецепта."""

    def get_recipe_filters(self, user):
        """Добавляет аннотации о том, добавлен ли рецепт в избранное
        пользователем и находится ли он в его корзине покупок."""
        return self.annotate(
            is_favorited=Exists(Favorite.objects.filter(
                user_id=user.id,
                recipe__id=OuterRef('pk')
            )),
            is_in_shopping_cart=Exists(ShoppingCart.objects.filter(
                user_id=user.id,
                recipe__id=OuterRef('pk')
            ))
        ).order_by('-pub_date')


class Recipe(models.Model):
    """Модель рецептов."""
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги',
        through='TagRecipe',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=MAX_STR_LENGTH,
    )
    text = models.TextField(
        'Описание рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        validators=[
            MinValueValidator(
                MIN_VALUE,
                f'Время приготовления должно быть '
                f'не менее {MIN_VALUE} минуты.'
            ),
            MaxValueValidator(
                MAX_COOKING_TIME,
                f'Время приготовления должно быть '
                f'не более {MAX_COOKING_TIME} минут.'
            )],
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
    )
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)

    objects = RecipeQuerySet.as_manager()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = '%(class)ss'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name[:STR_RETURN_VALUE]


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        'Название ингредиента',
        max_length=MAX_STR_LENGTH,
        help_text='Не более двухсот символов.'
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAX_STR_LENGTH,
        help_text='Не более двухсот символов.'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        default_related_name = '%(class)ss'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='%(app_label)s_%(class)s уже существует.',
            )
        ]

    def __str__(self):
        return self.name[:STR_RETURN_VALUE]


class Favorite(UserRecipeBaseModel):
    """Модель избранного."""
    class Meta(UserRecipeBaseModel.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избранное.'


class ShoppingCart(UserRecipeBaseModel):
    """Модель списка покупок."""
    class Meta(UserRecipeBaseModel.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (f'{self.user.username} добавил'
                f' {self.recipe.name} в список покупок.')


class RecipeIngredient(models.Model):
    """Модель ингредиенты рецепта."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество ингредиентов',
        validators=[
            MinValueValidator(
                MIN_VALUE,
                'Количество ингредиентов должно быть'
                f' не менее {MIN_VALUE}.'
            ),
            MaxValueValidator(
                MAXIMUM_AMOUNT_ALLOWED,
                'Количество ингредиентов должно быть'
                f' не более {MAXIMUM_AMOUNT_ALLOWED}.'
            ),
        ]
    )

    class Meta:
        default_related_name = '%(class)ss'
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return self.recipe.name[:STR_RETURN_VALUE]


class TagRecipe(models.Model):
    """Модель теги рецепта."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег',
    )

    class Meta:
        default_related_name = '%(class)ss'
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'

    def __str__(self):
        return self.tag.name[:STR_RETURN_VALUE]
