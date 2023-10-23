import base64  # Модуль с функциями кодирования и декодирования base64
import webcolors

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Count, Prefetch
from django.db import transaction
from rest_framework import serializers
from djoser.serializers import UserSerializer

from recipes.models import (Ingredient,
                            IngredientRecipe, Recipe, Tag,
                            TagRecipe, Subscription)

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    # pagination_class = None

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        if not self.context['subscriptions']:
            return False
        return obj.id in self.context.get('subscriptions', [])
        # return False


class IngredientsSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('name', 'measurement_unit', 'id')
        model = Ingredient


class IngredientRecipePostSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit.name')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class Hex2NameColor(serializers.Field):
    # При чтении данных ничего не меняем - просто возвращаем как есть
    def to_representation(self, value):
        return value
    # При записи код цвета конвертируется в его название
    def to_internal_value(self, data):
        # Доверяй, но проверяй
        try:
            # Если имя цвета существует, то конвертируем код в название
            data = webcolors.hex_to_name(data)
        except ValueError:
            # Иначе возвращаем ошибку
            raise serializers.ValidationError('Для этого цвета нет имени')
        # Возвращаем данные в новом формате
        return data


class TagsSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()  # Вот он - наш собственный тип поля
    
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Если полученный объект строка, и эта строка 
        # начинается с 'data:image'...
        if isinstance(data, str) and data.startswith('data:image'):
            # ...начинаем декодировать изображение из base64.
            # Сначала нужно разделить строку на части.
            format, imgstr = data.split(';base64,')  
            # И извлечь расширение файла.
            ext = format.split('/')[-1]  
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    ingredients = IngredientRecipeSerializer(source='ingredients_recipes', many=True)
    author = CustomUserSerializer(default=serializers.CurrentUserDefault())
    image = Base64ImageField() # required=False, allow_null=True

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time')


class RecipesShortSerializer(RecipesSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipesPostSerializer(RecipesSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = IngredientRecipePostSerializer(many=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault()) # 
    image = Base64ImageField(required=False, allow_null=True)

    class Meta: # 
        model = Recipe #
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time') # 
        read_only_fields = ('author',) # 

    # @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        lst = []
        for tag in tags:
            TagRecipe.objects.create(tag=tag, recipe=recipe)
            lst.append(tag)
        recipe.tags.set(lst)
        IngredientRecipe.objects.bulk_create(
            [IngredientRecipe(ingredient=ingredient['id'], recipe=recipe,
                              amount=ingredient['amount'])
             for ingredient in ingredients])
        return recipe

    # @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            TagRecipe.objects.filter(recipe_id=instance.id).delete()
            lst = []
            for tag in tags_data:
                TagRecipe.objects.create(tag=tag, recipe=instance)
                lst.append(tag)
            instance.tags.set(lst)
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            IngredientRecipe.objects.filter(recipe_id=instance.id).delete()
            IngredientRecipe.objects.bulk_create(
                [IngredientRecipe(ingredient=ingredient['id'], recipe=instance,
                                  amount=ingredient['amount'])
                 for ingredient in ingredients_data])
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipesSerializer(instance, context=self.context)
        return serializer.data


class SubscriptionSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.method == 'POST':
            recipes = obj.recipes.all()
        else:
            recipes_all = self.context.get('recipes', [])
            recipes = recipes_all.filter(author=obj)
        if request:
            recipes_limit = request.GET.get("recipes_limit")
            if recipes_limit:
                recipes = recipes[:int(recipes_limit)]
        serializer = RecipesShortSerializer(recipes, many=True)
        return serializer.data
    
"""
class SubscribeSerializer(serializers.ModelSerializer): # ryb
    id = serializers.SlugRelatedField(
        slug_field="id", queryset=User.objects.all(), source="author"
    )
    print("id", id)
    subscriber = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    print("sub", subscriber)

    class Meta:
        fields = ["id", "subscriber"]
        model = Subscription

    def create(self, validated_data):
        print("validated_data", validated_data)
        if "subscriber" not in validated_data:
            validated_data["subscriber"] = self.context["request"].user
        return Subscription.objects.create(**validated_data)

"""

class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ()
        model = Subscription

    def validate(self, data):
        request = self.context.get('request')
        author = get_object_or_404(
            User,
            pk=self.context.get('view').kwargs.get('id')
        )
        subscriber = request.user
        if request.method == 'POST':
            if author == subscriber:
                raise serializers.ValidationError(
                    'Нельзя подписаться на самого себя!')
            if Subscription.objects.filter(author=author,
                                           subscriber=subscriber
                                           ).exists():
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого автора!')
        return data

    def to_representation(self, instance):
        user_query = User.objects.all().annotate(
            recipes_count=Count('recipes'))
        sub_query = Subscription.objects.select_related(
            'subscriber').prefetch_related(Prefetch('author',
                                                    queryset=user_query))
        instance = get_object_or_404(sub_query, subscriber=instance.subscriber,
                                     author=instance.author)
        serializer = SubscriptionSerializer(instance.author,
                                            context=self.context)
        return serializer.data
