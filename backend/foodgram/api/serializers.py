from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorites, Follow, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CharField,
                                        CurrentUserDefault,
                                        HiddenField,
                                        ImageField,
                                        IntegerField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        ReadOnlyField,
                                        SerializerMethodField,
                                        StringRelatedField)

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
        return Follow.objects.filter(
            user=not user.is_anonymous, author=obj
        ).exists()

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


class RecipeIngredientSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(source='ingredient.id', read_only=True)
    name = StringRelatedField(source='ingredient.name', read_only=True)
    measurement_unit = StringRelatedField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class SmallRecipeSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image',)


class RecipeListSerializer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserFoodgramSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        read_only=True,
        many=True,
        source='recipe_ingredients'
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

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
            'cooking_time'
        )

    def get_request_user(self, model, obj):
        user_id = self.context.get('request').user.id
        return model.objects.filter(author=user_id, recipe=obj.id).exists()

    def get_is_favorited(self, obj):
        return self.get_request_user(Favorites, obj)

    def get_is_in_shopping_cart(self, obj):
        return self.get_request_user(ShoppingCart, obj)


class AddIngredientSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeWriteSerializer(ModelSerializer):
    ingredients = AddIngredientSerializer(
        many=True,
        write_only=True)
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
    author = HiddenField(
        default=CurrentUserDefault()
    )

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author'
        )

    def to_representation(self, instance):
        ingredients = super().to_representation(instance)
        ingredients['ingredients'] = RecipeIngredientSerializer(
            instance.recipe_ingredients.all(), many=True
        ).data
        return ingredients

    def add_tags_ingredients(self, ingredients, tags, model):
        for ingredient in ingredients:
            RecipeIngredient.objects.update_or_create(
                recipe=model,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
        model.tags.set(tags)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        self.add_tags_ingredients(ingredients, tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        self.add_tags_ingredients(ingredients, tags, instance)
        return super().update(instance, validated_data)


class AbsrtactSerializer(ModelSerializer):
    name = ReadOnlyField(
        source='recipe.name',
        read_only=True
    )
    image = ImageField(
        source='recipe.image',
        read_only=True
    )
    coocking_time = IntegerField(
        source='recipe.cooking_time',
        read_only=True
    )
    id = PrimaryKeyRelatedField(
        source='recipe',
        read_only=True
    )


class ShoppingCartSerializer(AbsrtactSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'coocking_time')


class FavoritesSerializer(AbsrtactSerializer):

    class Meta:
        model = Favorites
        fields = ('id', 'name', 'image', 'coocking_time')


class FollowSerializer(UserFoodgramSerializer):
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.author)
        if limit and limit.isdigit():
            recipes = recipes[:int(limit)]
        return SmallRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def validate(self, data):
        author = self.context.get('author')
        user = self.context.get('request').user
        if Follow.objects.filter(
                author=author,
                user=user
        ).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST)
        if user == author:
            raise ValidationError(
                detail='Невозможно подписаться на себя!',
                code=status.HTTP_400_BAD_REQUEST)
        return data
