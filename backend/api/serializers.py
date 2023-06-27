import base64
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import User, Subscribe
from recipes.models import (
    Tag, Ingredient, Recipes, Favorite, ShoppingCart, AmountIngredient
    )
from rest_framework.fields import RegexField


class CreateUserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name',)
        extra_kwargs = {'password': {'write_only': True}}


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscribe.objects.filter(user=user, author=obj).exists()
        return False


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='author.id')
    email = serializers.EmailField(source='author.email')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            )


class TagSerializer(serializers.ModelSerializer):
    color = serializers.CharField(
        validators=[RegexField(r'^#[0-9a-fA-F]{6}$')],
        error_messages={'invalid': 'Введите корректный цвет в формате #RRGGBB'}
        )

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class GetAmountIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(
        source='ingredient.name',
        required=False
        )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        required=False
        )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class PostAmountIngredientSerializer(GetAmountIngredientSerializer):

    class Meta(GetAmountIngredientSerializer.Meta):
        model = AmountIngredient
        fields = ('id', 'amount',)


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(many=False, read_only=True)
    ingredients = GetAmountIngredientSerializer(
        many=True,
        source='amount_recipe'
        )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
            )

    def get_is_favorited(self, obj):
        user = self.context['request'].user.id
        return Favorite.objects.filter(
            user=user, recipe=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user.id
        return ShoppingCart.objects.filter(
            user=user, recipe=obj.id
        ).exists()


class Base64ImageField(serializers.ImageField):
    """Сериалайзер для преобразования картинки с фронтенда."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipesPostUpdateSerializer(RecipesSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('amount_recipe')
        recipe = Recipes.objects.create(
            author=self.context['request'].user, **validated_data
            )
        for tag in tags_data:
            recipe.tags.add(tag)
        for ingredient_data in ingredients_data:
            pk = ingredient_data['ingredient']['id']
            ingredient = Ingredient.objects.get(pk=pk)
            amount = ingredient_data['amount']
            print(ingredients_data)
            AmountIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
                )
        return recipe

    # class Meta(RecipesSerializer.Meta):
    #     model = Recipes
    #     fields = (
    #         'id',
    #         'tags',
    #         'author',
    #         'ingredients',
    #         'is_favorited',
    #         'is_in_shopping_cart',
    #         'name',
    #         'image',
    #         'text',
    #         'cooking_time',
    #         )
