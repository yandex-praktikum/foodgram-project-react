
from django.contrib.auth import get_user_model
from django.db.models import F
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import Tag, Recipe, RecipeIngredient, Ingredient



User = get_user_model()





class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'



class ProfileSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'username','id'
        )



class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    amount = serializers.IntegerField(min_value=1, max_value=10000)
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'amount', 'measurement_unit')



    

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True, source='recipe_ingredients')

    class Meta:
        model = Recipe
        fields = '__all__'


class GetIngredientsMixin:
    """Миксина для рецептов, получение ингредиентов"""

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit',
            amount=F('recipe_ingredients__amount')
        )


class RecipeCreateSerializer(GetIngredientsMixin, serializers.ModelSerializer):
    """Сериализатор для записи рецепта"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = serializers.SerializerMethodField()
    

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

    def validate(self, data):
        ingredients = self.initial_data['ingredients']
        ingredient_list = []
        if not ingredients:
            raise serializers.ValidationError(
                'Минимально должен быть 1 ингредиент.'
            )
        for item in ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=item['id']
            )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиент не должен повторяться.'
                )
            if int(item.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Минимальное количество = 1'
                )
            ingredient_list.append(ingredient)
        data['ingredients'] = ingredients
        return data

    def validate_cooking_time(self, time):
        if int(time) < 1:
            raise serializers.ValidationError(
                'Минимальное время = 1'
            )
        return time

    def add_ingredients_and_tags(self, instance, **validate_data):
        ingredients = validate_data['ingredients']
        tags = validate_data['tags']
        for tag in tags:
            instance.tags.add(tag)

        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients
        ])
        return instance

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        return self.add_ingredients_and_tags(
            recipe, ingredients=ingredients, tags=tags
        )

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = self.add_ingredients_and_tags(
            instance, ingredients=ingredients, tags=tags)
        return super().update(instance, validated_data)


"""
class RecipeCreateSerializer(serializers.ModelSerializer):
    # ingredients = RecipeIngredientSerializer(many=True)
    cooking_time = serializers.IntegerField(min_value=1, max_value=1000)
    author = ProfileSerializers(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'text', 'cooking_time')
        

    def validate(self, data):
        ingredients = self.initial_data['ingredients']
        ingredient_list = []
        if not ingredients:
            raise serializers.ValidationError(
                'Минимально должен быть 1 ингредиент.'
            )
        for item in ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=item['id']
            )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиент не должен повторяться.'
                )
            if int(item.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Минимальное количество = 1'
                )
            ingredient_list.append(ingredient)
        data['ingredients'] = ingredients
        return data

    def add_ingredients_and_tags(self, instance, **validate_data):
        ingredients = validate_data['ingredients']
        tags = validate_data['tags']
        for tag in tags:
            instance.tags.add(tag)

        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients
        ])
        return instance

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        return self.add_ingredients_and_tags(
            recipe, ingredients=ingredients, tags=tags
        )



    def create(self, validated_data):
    # Уберем список достижений из словаря validated_data и сохраним его
        ingredients = validated_data.pop('ingredients')

        # Создадим нового котика пока без достижений, данных нам достаточно
        recipe = Recipe.objects.create(**validated_data)

        # Для каждого достижения из списка достижений
        for ingredient in ingredients:
            # Создадим новую запись или получим существующий экземпляр из БД
            current_ingredient = Ingredient.objects.get_or_create(
                **ingredient)
            # Поместим ссылку на каждое достижение во вспомогательную таблицу
            # Не забыв указать к какому котику оно относится
            RecipeIngredient.objects.create(
                ingredient=current_ingredient, recipe=recipe)
        return recipe

"""