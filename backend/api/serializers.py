from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Ingredients, Recipes, Tags

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


class UserSerializer(serializers.ModelSerializer, IsSubscribedMixin):

    class Meta:
        model = User
        fields = ('email', 'pk', 'username', 'first_name', 'last_name',
                  'is_subscribed')


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = '__all__'


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = '__all__'


class RecipesSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagsSerializer(required=False, many=True)
    ingredients = IngredientsSerializer(required=False, many=True)
    author = UserSerializer(read_only=True)

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
