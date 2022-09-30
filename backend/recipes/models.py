from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import CustomUser

User = CustomUser


class Tags(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Имя тега', unique=True)
    color = models.CharField(max_length=7,
                             verbose_name='цвет', unique=True)
    slug = models.SlugField(max_length=200,
                            verbose_name='слаг', unique=True)

    class Meta:
        verbose_name = 'Tag'

    def __str__(self):
        return f'{self.name}, {self.color}, {self.slug}'


class Ingredients(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=20,
                                        verbose_name='Единица измерения',)

    class Meta:
        verbose_name = 'Ingredient'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор рецепта',
                               related_name='recipes',)
    ingredients = models.ManyToManyField(Ingredients,
                                         related_name='ingredients',
                                         through='IngredientAmount',
                                         verbose_name='Ингредиенты',)
    tags = models.ManyToManyField(Tags, related_name='tags',
                                  verbose_name='Хэштег',)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                    db_index=True)
    text = models.TextField(verbose_name='Описание',
                            max_length=1000)
    name = models.CharField(max_length=200, verbose_name='Название',)
    image = models.ImageField(upload_to='media/', verbose_name='Изображение',)
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1, 'Значение не может быть меньше 1')],
        verbose_name='Время готовки в минутах',

    )

    class Meta:
        verbose_name = 'Recipe'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name

    @property
    def favorited_count(self):
        return self.favorited.aggregate(models.Count('id'))['id__count']


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, related_name='favorites',
                               on_delete=models.CASCADE)
    added = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления в избранное'
    )

    class Meta:
        verbose_name = 'Favorite'
        UniqueConstraint(fields=['recipe', 'user'], name='favorite_unique')

    def __str__(self):
        return f"{self.user} has favorites: {self.recipe.name}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_shopping_list',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                               related_name='purchases',
                               verbose_name='Покупка')
    added = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления в список покупок'
    )

    class Meta:
        verbose_name = 'ShopList'

    def __str__(self):
        return f'In {self.user} shopping list: {self.recipe}'


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredients, on_delete=models.CASCADE,
        related_name='ingredients_in_recipe', verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE,
        related_name='recipes_ingredients_list', verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)],
        verbose_name='Количество ингредиентов'
    )

    class Meta:
        verbose_name = 'IngAmount'

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'
