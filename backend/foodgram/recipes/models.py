from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, CharField, DateField, ForeignKey,
                              ImageField, ManyToManyField, Model,
                              PositiveIntegerField, SlugField, TextField,
                              UniqueConstraint)

from users.models import UserFoodgram


class Ingredient(Model):
    name = CharField(
        verbose_name='Название ингредиента',
        help_text='Введите ингредиент',
        max_length=200
    )
    measurement_unit = CharField(
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения',
        max_length=200
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Tag(Model):
    name = CharField(
        verbose_name='Название тега',
        help_text='Введите название тега',
        max_length=200,
        unique=True
    )
    color = CharField(
        verbose_name='Цвет в НЕХ',
        help_text='Выбирите цвет',
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )
    slug = SlugField(
        verbose_name='Слаг тега',
        help_text='Введите слаг тега',
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'


class Recipe(Model):
    tags = ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
        help_text='Выбирите теги'
    )
    author = ForeignKey(
        UserFoodgram,
        related_name='recipes',
        verbose_name='Автор рецепта',
        on_delete=CASCADE
    )
    ingredients = ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиенты',
        help_text='Введите игредиенты',
        through='RecipeIngredient'
    )
    name = CharField(
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
        max_length=200
    )
    image = ImageField(
        verbose_name='Картинка рецепта',
        help_text='Добавьте изображение',
        upload_to='media/'
    )
    text = TextField(
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта'
    )
    cooking_time = PositiveIntegerField(
        verbose_name='Время приготовления(в минутах)',
        help_text='Укажите время в минутах',
        validators=[MinValueValidator(1, 'Минимальное время приготовления')]
    )
    pub_date = DateField(verbose_name='Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe')]

    def __str__(self):
        return f'{self.name}'


class RecipeIngredient(Model):
    ingredient = ForeignKey(
        Ingredient,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент',
        help_text='Укажите инредиенты',
        on_delete=CASCADE
    )
    recipe = ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
        help_text='Укажите рецепт',
        on_delete=CASCADE
    )
    amount = PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, 'Минимальное количество ингредиентов 1')],
        help_text='Укажите количество ингредиентов'
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Игредиенты рецепта'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient')]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class AbstractModel(Model):
    author = ForeignKey(
        UserFoodgram,
        verbose_name='Пользователь',
        on_delete=CASCADE
    )
    recipe = ForeignKey(
        Recipe,
        verbose_name='Рецепт для приготовления',
        help_text='Выберите рецепт для приготовления',
        on_delete=CASCADE
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.recipe}'


class ShoppingCart(AbstractModel):

    class Meta:
        default_related_name = 'shopping_cart'
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [UniqueConstraint(
            fields=['author', 'recipe'],
            name='unique_cart')]


class Favorites(AbstractModel):

    class Meta:
        default_related_name = 'favorites'
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [UniqueConstraint(
            fields=['author', 'recipe'],
            name='unique_favorites')]


class Follow(Model):
    user = ForeignKey(
        UserFoodgram,
        related_name='follower',
        verbose_name='Пользователь',
        on_delete=CASCADE,
    )
    author = ForeignKey(
        UserFoodgram,
        related_name='followed',
        verbose_name='Автор',
        on_delete=CASCADE
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following')]

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
