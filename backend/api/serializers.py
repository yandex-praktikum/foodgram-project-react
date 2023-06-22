from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from foodgram_backend.settings import PASSWORD_MAX_LENGTH
from recipes.models import Ingredients, Recipes, Tags, RecipeIngredient

User = get_user_model()


class IsSubscribedMixin(serializers.Serializer):
    '''Mixin для проверки наличия подписки пользователя на автора
    '''
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context['request']

        if request.user.is_authenticated:
            # Если запрошен список пользователей.
            if isinstance(obj, User):
                return request.user.follower.filter(following=obj.id).exists()

        return False


class UserGetSerializer(serializers.ModelSerializer, IsSubscribedMixin):

    class Meta:
        model = User
        fields = ('email', 'pk', 'username', 'first_name', 'last_name',
                  'is_subscribed')


class UserCreateSerializer(serializers.ModelSerializer, IsSubscribedMixin):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',)


class SetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={"input_type": "password"},
        max_length=PASSWORD_MAX_LENGTH
    )
    new_password = serializers.CharField(
        style={"input_type": "password"},
        max_length=PASSWORD_MAX_LENGTH
    )

    default_error_messages = {
        "invalid_password": 'Неверный пароль'
    }

    def validate_current_password(self, value):
        is_password_valid = self.context['request'].user.check_password(value)
        if is_password_valid:
            return value
        else:
            self.fail("invalid_password")


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = '__all__'


class RecipeIngredientGetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.pk')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = '__all__'


class RecipesGetSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagsSerializer(required=False, many=True)
    ingredients = RecipeIngredientGetSerializer(
        required=False,
        many=True,
        source='ingredientrecipes',)
    author = UserGetSerializer(read_only=True)

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context['request']

        if request.user.is_authenticated:
            return request.user.lover.filter(recipe=obj.id).exists()

        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']

        if request.user.is_authenticated:
            return request.user.buyer.filter(recipe=obj.id).exists()

        return False


class RecipesPostSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True)
    image = Base64ImageField(use_url=False,)
    ingredients = RecipeIngredientPostSerializer(
        many=True,
        source='ingredientrecipes',)

    class Meta:
        model = Recipes
        fields = ('tags', 'ingredients', 'name', 'image', 'text',
                  'cooking_time')
