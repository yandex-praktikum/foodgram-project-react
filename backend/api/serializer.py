from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        ReadOnlyField, IntegerField, IntegerField, PrimaryKeyRelatedField, ImageField)
from djoser.serializers import UserSerializer
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

from recipes.models import (
    Tag,
    Recipe,
    Ingredient,
    IngredientInRecipe,
    Favorites,
    ShopCart,
    TagInRecipe

)
from users.models import UserFoodgram, Fallow


class Base64ImageField(ImageField):
    """Кастомное поле для кодирования изображения в base64."""

    def to_internal_value(self, data):
        """Метод преобразования картинки"""

        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='photo.' + ext)

        return super().to_internal_value(data)


class TagSerializer(ModelSerializer):
    """Сериализатор для тэгов"""
    class Meta:
        """Метамодель сериализатора TagSerializer"""
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientInRecipeSerializer(ModelSerializer):
    """Сериализатор для IngredientInRecipe"""

    id = ReadOnlyField(
        source='ingredient.id'
    )
    name = ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        """Мета-параметры сериализатора"""

        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class UserFoodgramSerializer(ModelSerializer):
    """Сериализатор для юзеров"""
    is_follower = SerializerMethodField()

    class Meta:
        model = UserFoodgram
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_follower",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def get_is_follower(self, obj):
        """Проверка состояния подписки"""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Fallow.objects.filter(
            user=user, auhtor=obj.id
        ).exists()


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов"""
    tag = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = IngredientInRecipeSerializer(
        source='ingredient_list', many=True
    )
    is_favirite = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tag', 'author',
                  'ingredients', 'is_favirite',
                  'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time',
                  'created'
                  )
        read_only_fields = (
            'is_favirite', 'is_in_shopping_cart'
        )

    def get_is_favorite(self, obj):
        """Присутствие в избранном"""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorites.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        """Присутствие в корзине """
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShopCart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()


class IngredientSerializer(ModelSerializer):
    """Сериализатор для ингридиентов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class CreateIngredientsInRecipeSerializer(ModelSerializer):
    """Сериализатор для ингредиентов в рецептах"""
    id = IntegerField()
    amount = IntegerField()

    @staticmethod
    def validate_amount(value):
        """Метод валидации количества"""
        if value < 1:
            raise ValidationError(
                'Должна быть минимум одна единицп ингридиента в рецепте!'
            )
        return value

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class CreateRecipeSerializer(ModelSerializer):
    """Сериализатор для создания рецептов"""

    ingredients = CreateIngredientsInRecipeSerializer(many=True)
    tags = PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'name',
                  'image', 'text', 'cooking_time')

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )
        return serializer.data

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        lst_ingredient = []

        for ingredient in ingredients:
            if ingredient['id'] in lst_ingredient:
                raise ValidationError(
                    'Такой ингридиент уже есть'
                )
            lst_ingredient.append(ingredient['id'])

        return data

    def create_ingredients(self, ingredients, recipe):
        for element in ingredients:
            id = element['id']
            ingredient = Ingredient.objects.get(pk=id)
            amount = element['amount']
            IngredientInRecipe.objects.create(
                ingredient=ingredient, recipe=recipe, amount=amount
            )

    def create_tags(self, tags, recipe):
        recipe.tags.set(tags)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tag')

        user = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data, author=user)
        self.create_ingredients(ingredients, recipe)
        self.create_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        TagInRecipe.objects.filter(recipe=instance).delete()

        self.create_ingredients(validated_data.pop('ingredients'), instance)
        self.create_tags(validated_data.pop('tag'), instance)

        return super().update(instance, validated_data)


class CreateUserFoodgramSerializer(UserFoodgramSerializer):
    """Сериализатор для создания пользователя
    без проверки на подписку """

    class Meta:
        model = UserFoodgram
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'password'
                  )
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AdditionalForRecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(UserFoodgramSerializer):
    recipes = SerializerMethodField(
        read_only=True,
        method_name='get_recipes')
    recipes_count = SerializerMethodField(
        read_only=True
    )

    class Meta:
        """Мета-параметры сериализатора"""
        model = UserFoodgram
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return AdditionalForRecipeSerializer(recipes, many=True).data

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes.count()


class AddFavoritesSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        """Мета-параметры сериализатора"""

        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
