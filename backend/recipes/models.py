from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models

from foodgram.constants import CHAR_FIELD_MAX_LENGTH, COLOR_FIELD_MAX_LENGTH


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=CHAR_FIELD_MAX_LENGTH
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=CHAR_FIELD_MAX_LENGTH
    )

    class Meta:
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='Уникальность ингредиентов'
            )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'Название',
        unique=True,
        max_length=CHAR_FIELD_MAX_LENGTH
    )
    color = ColorField(
        'Цвет в НЕХ',
        unique=True,
        max_length=COLOR_FIELD_MAX_LENGTH
    )
    slug = models.SlugField(
        'Уникальный слаг',
        unique=True,
        max_length=CHAR_FIELD_MAX_LENGTH
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        'Название',
        max_length=CHAR_FIELD_MAX_LENGTH
    )
    image = models.ImageField(
        'Ссылка на картинку',
        upload_to='recipes/media'
    )
    text = models.TextField('Описание')
    cooking_time = models.PositiveIntegerField(
        'Время приготовления в мин',
        validators=[
            MinValueValidator(1, message='Мин. значение - 1!'),
        ]
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Список тэгов'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепты автора',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='ingredients',
        verbose_name='Ингредиенты'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes_ingredient'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[
            MinValueValidator(1, message='Минимальное значение - 1!')
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='Уникальность ингредиентов в рецепте'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}!'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='Уникальность подписок'
            )
        ]


    def clean(self):
        if self.user == self.following:
            raise ValidationError('Вы не можете подписаться на самого себя!')


    def __str__(self):
        return f'Подписка {self.user} на {self.following}!'


class AbstractModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
    

    def clean(self):
        if self.__class__.objects.filter(user=self.user, recipe=self.recipe).exists():
            raise ValidationError('Такая запись уже существует!')


class Favorites(AbstractModel):
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Уникальность избранного'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил рецепт {self.recipe} в избранное!'


class ShoppingCart(AbstractModel):
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shoppingcart'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Уникальность покупок'
            )
        ]

    def __str__(self):
        return (
            f'Рецепт {self.recipe} в списке покупок у {self.user}!'
        )
