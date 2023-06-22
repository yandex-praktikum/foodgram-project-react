from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import User, Subscribe
from recipes.models import Tag, Ingredient
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
        return Subscribe.objects.filter(
            user=user, author=obj
        ).exists() if user.is_authenticated else False


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
