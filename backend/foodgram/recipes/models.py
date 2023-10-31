from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
# from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token



class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True)
    password = models.CharField(
        _('password'),
        max_length=150)
    first_name = models.CharField(
        _('first name'),
        max_length=150)
    last_name = models.CharField(
        _('last name'),
        max_length=150)


    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['pk']
        verbose_name = 'поварёнок'
        verbose_name_plural = 'Все поварята'


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, null=True, unique=True)
    slug = models.SlugField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'В какое время подавать'
        verbose_name = 'В какое время подавать'

    # def get_absolute_url(self):
        # return reverse('api/tags/', kwargs={'tag_slug': self.slug})


class Recipe(models.Model):
    name = models.CharField(max_length=100, verbose_name = 'Название')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата публикации')
    text = models.TextField(verbose_name = 'Как приготовить')
    cooking_time = models.IntegerField(validators=[MinValueValidator(1, 'Время не может быть меньше 1 минуты.')],
                                       verbose_name = 'Время готовки')
    image = models.ImageField(upload_to='recipes/images/', verbose_name = 'Вариант сервировки')
    tags = models.ManyToManyField(Tag, related_name='recipes', verbose_name = 'В какое время подавать')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes', verbose_name = 'Имя поварёнка')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe',
                                         related_name='recipes', verbose_name = 'Ингредиенты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
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

    class Meta:
        ordering = ['-recipe']


class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')

    class Meta:
        verbose_name_plural = 'Подписки'
        ordering = ['author']
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'author'],
                                    name='unique subscriber author')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe')

    class Meta:
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ['user']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique user recipe')
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='cart')

    class Meta:
        verbose_name= 'Список покупок'
        verbose_name_plural = 'Список покупок'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique user cart')
        ]
