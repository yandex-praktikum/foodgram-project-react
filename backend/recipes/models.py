from django.db import models
# from django.core.validators import MinValueValidator

# from users.models import User


class Tag(models.Model):
    """Модель хранения информациия о тегах"""
    name = models.CharField(
        verbose_name='Тег',
        max_length=100,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
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


# class Ingredient(models.Model):
#     """Модель хранения информациия о ингредиентах"""
#     name = models.CharField(
#         'Ингредиент',
#         max_length=200,
#         db_index=True,
#         verbose_name='Ингредиент')
#     measurement_unit = models.CharField(
#         max_length=200,
#         verbose_name='Единицы измерения')

#     class Meta:
#         ordering = ('name',)
#         verbose_name = 'Ингредиент'
#         verbose_name_plural = 'Ингредиенты'

#     def __str__(self):
#         return f'{self.name}, {self.measurement_unit}'


# class Recipe(models.Model):
#     """Модель хранения информациия о рецептаx"""
#     author = models.ForeignKey(
#         User,
#         related_name='recipes',
#         on_delete=models.CASCADE,
#         verbose_name='Автор рецепта',
#     )
#     name = models.CharField(
#         max_length=200,
#         verbose_name='Название рецепта'
#     )
#     image = models.ImageField(
#         verbose_name='Фотография рецепта',
#         upload_to='recipes/',
#         blank=True
#     )
#     text = models.TextField(
#         verbose_name='Описание рецепта'
#     )
#     ingredients = models.ManyToManyField(
#         Ingredient,
#         through='IngredientInRecipe',
#         related_name='recipes',
#         verbose_name='Ингредиенты'
#     )
#     tags = models.ManyToManyField(
#         Tag,
#         related_name='recipes',
#         verbose_name='Теги'
#     )
#     cooking_time = models.PositiveSmallIntegerField(
#         'Время приготовления',
#         validators=[
#             MinValueValidator(1, message='Минимальное значение 1!'),
#         ]
#     )
#     created = models.DateTimeField(
#         auto_now_add=True,
#         db_index=True,
#         verbose_name='Дата публикации рецепта'
#     )

#     class Meta:
#         verbose_name = 'Рецепт'
#         verbose_name_plural = 'Рецепты'
#         ordering = ('-created',)

#     def __str__(self):
#         return self.name
