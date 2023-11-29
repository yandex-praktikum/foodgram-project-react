# from core.utils import ingredient_recipe
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from recipes.models import (Ingredient, IngredientRecipe,
                            Recipe, Tag, TagRecipe,
                            ShoppingCart, FavoriteRecipe)
from users.models import User, Subscription


class GetIsSubscribedMixin:
    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return user.subscriber.filter(author=obj.id).exists()


class CustomUserSerializer(GetIsSubscribedMixin, UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name",
                  "is_subscribed")
        read_only_fields = ("is_subscribed",)


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "measurement_unit", "id")
        model = Ingredient


class IngredientRecipePostSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            if int(ingredient.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Некорректное количество ингредиента')
        return data

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredient.id")
    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    ingredients = IngredientRecipeSerializer(source="ingredients_recipes",
                                             many=True)
    author = CustomUserSerializer(default=serializers.CurrentUserDefault())
    image = Base64ImageField(
        required=False, allow_null=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
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
        return (self.context.get('request').user.is_authenticated
                and FavoriteRecipe.objects.filter(
                    user=self.context.get('request').user,
                    favorite_recipe=obj
        ).exists())
    
    def get_is_in_shopping_cart(self, obj):
        return (self.context.get('request').user.is_authenticated
                and ShoppingCart.objects.filter(
                    user=self.context.get('request').user,
                    recipe=obj
        ).exists())



class RecipeMinifiedSerializer(RecipesSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class RecipesPostSerializer(RecipesSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = IngredientRecipePostSerializer(many=True)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = ("author",)

    def validate_tags(self, tags):
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    'Повтор тега'
                )
            tags_list.append(tag)
            if len(tags_list) < 1:
                raise serializers.ValidationError(
                    'Выберите тег'
                )
        return tags
    
    def validate_ingredients(self, data):
        if not data:
            raise serializers.ValidationError(
                'Выберите ингредиент'
            )
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиент выбран повторно'
                )
    


    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Минимальное время готовки не менее 1 минуты')
        if cooking_time > 300:
            raise serializers.ValidationError(
                'Время готовки ограничено 5 часами')
        return cooking_time

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientRecipe.objects.bulk_create([
                IngredientRecipe(
                    recipe=recipe,
                    ingredient_id=ingredient.get('id'),
                    amount=ingredient.get('amount'),)
            ])

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe




    """
    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        IngredientRecipe.objects.bulk_create(
            [IngredientRecipe(ingredient=ingredient['id'], recipe=recipe,
                              amount=ingredient['amount'])
             for ingredient in ingredients])
        return recipe
    """



    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        instance.image = validated_data.get("image", instance.image)
        if "tags" in validated_data:
            tags_data = validated_data.pop("tags")
            TagRecipe.objects.filter(recipe_id=instance.id).delete()
            lst = []
            for tag in tags_data:
                TagRecipe.objects.create(tag=tag, recipe=instance)
                lst.append(tag)
            instance.tags.set(lst)
        if "ingredients" in validated_data:
            ingredients_data = validated_data.pop("ingredients")
            IngredientRecipe.objects.filter(recipe_id=instance.id).delete()
            IngredientRecipe.objects.bulk_create(
                [
                    IngredientRecipe(
                        ingredient=ingredient["id"],
                        recipe=instance,
                        amount=ingredient["amount"],
                    )
                    for ingredient in ingredients_data
                ]
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipesSerializer(instance, context=self.context)
        return serializer.data


class SubscriptionSerializer(CustomUserSerializer):
    recipes = RecipeMinifiedSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = ("__all__",)

    def get_is_subscribed(*args):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ()
        model = Subscription

    def validate(self, data):
        request = self.context.get("request")
        author = get_object_or_404(
            User, pk=self.context.get("view").kwargs.get("id")
        )
        subscriber = request.user
        if request.method == "POST":
            if author == subscriber:
                raise serializers.ValidationError(
                    "Нельзя подписаться на самого себя!"
                )
            if Subscription.objects.filter(
                author=author, subscriber=subscriber
            ).exists():
                raise serializers.ValidationError(
                    "Вы уже подписаны на этого автора!"
                )
        return data

    def to_representation(self, instance):
        user_query = User.objects.all().annotate(
            recipes_count=Count("recipes")
        )
        sub_query = Subscription.objects.select_related(
            "subscriber").prefetch_related(
                Prefetch("author", queryset=user_query)
        )
        instance = get_object_or_404(
            sub_query, subscriber=instance.subscriber, author=instance.author
        )
        serializer = SubscriptionSerializer(instance.author,
                                            context=self.context)
        return serializer.data


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='favorite_recipe.id',
    )
    name = serializers.ReadOnlyField(
        source='favorite_recipe.name',
    )
    image = serializers.CharField(
        source='favorite_recipe.image',
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField(
        source='favorite_recipe.cooking_time',
    )

    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        user = self.context.get('request').user
        recipe = self.context.get('recipe_id')
        if FavoriteRecipe.objects.filter(user=user,
                                         favorite_recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Рецепт уже в избранном'})
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='recipe.id',
    )
    name = serializers.ReadOnlyField(
        source='recipe.name',
    )
    image = serializers.CharField(
        source='recipe.image',
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField(
        source='recipe.cooking_time',
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        user = self.context.get('request').user
        recipe = self.context.get('recipe_id')
        if ShoppingCart.objects.filter(user=user,
                                       recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Рецепт уже добавлен в список покупок'})
        return data
