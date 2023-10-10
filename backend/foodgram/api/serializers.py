
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from djoser.serializers import UserSerializer

from recipes.models import (Ingredient,
                            IngredientRecipe, Recipe, Tag,
                            TagRecipe)

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        #
        return False


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


class TagsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    ingredients = IngredientRecipeSerializer(source='ingredients_recipes', many=True)
    author = CustomUserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'text', 'cooking_time')


class RecipesPostSerializer(RecipesSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = IngredientRecipePostSerializer(many=True)

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
