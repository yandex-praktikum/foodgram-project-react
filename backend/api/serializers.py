from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Ingredients, Tags

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'pk', 'username', 'first_name', 'last_name')


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ('pk', 'name', 'measurement_unit')


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('pk', 'name', 'color', 'slug')
