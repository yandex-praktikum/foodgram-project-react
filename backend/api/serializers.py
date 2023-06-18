from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Ingredients, Tags

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
        fields = ('pk', 'name', 'measurement_unit')


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('pk', 'name', 'color', 'slug')
