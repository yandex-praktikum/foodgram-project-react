from recipes.models import (Favorite, Follow, Ingredient, Recipe,
                            RecipeIngredient, Tag)
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CharField, CurrentUserDefault,
                                        HiddenField, ImageField, IntegerField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField)
from users.models import UserFoodgram


class UserFoodgramSerializer(ModelSerializer):
    password = CharField(write_only=True)
    is_subscribed = SerializerMethodField()

    class Meta:
        model = UserFoodgram
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed'
        )
        write_only_fields = ('password',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Follow.objects.filter(user=user, author=obj).exists()
        return False

    def create(self, validated_data):
        user = UserFoodgram.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name,', 'measurement_unit')


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')
