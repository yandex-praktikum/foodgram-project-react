from users.models import User, Subscribe
from djoser.views import UserViewSet
from .serializers import (
    CustomUserSerializer, SubscribeSerializer, TagSerializer,
    IngredientSerilizer, RecipesPostUpdateSerializer, RecipesSerializer,
    CartSerializer
    )
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from recipes.models import Tag, Ingredient, Recipes, ShoppingCart, Favorite
import csv
from django.http import HttpResponse


class UsersViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    search_fields = ('username', 'email')
    permission_classes = (AllowAny,)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = SubscribeSerializer(
                Subscribe.objects.create(user=request.user, author=author),
                context={'request': request},
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        Subscribe.objects.filter(user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)

    @action(detail=False)
    def get_tag(self, request):
        tag = Tag.objects.all()
        serializer = self.get_serializer(tag, many=True)
        return Response(serializer.data)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerilizer
    permission_classes = (AllowAny,)

    @action(detail=False)
    def get_ingredients(self, request):
        ingredient = Ingredient.objects.all()
        serializer = self.get_serializer(ingredient, many=True)
        return Response(serializer.data)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesSerializer
        return RecipesPostUpdateSerializer

    @action(detail=False, methods=['get'], permission_classes=(AllowAny,))
    def get_recipes(self, request):
        recipes = Recipes.objects.all()
        serializer = RecipesSerializer(recipes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post', 'patch', 'delete'])
    def post_recipes(self, request):
        serializer = RecipesPostUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipes, pk=pk)
        cart = ShoppingCart.objects.filter(user=user, recipe=recipe)

        if self.request.method == "POST":
            if cart:
                return Response(
                    {'error': 'Рецепт уже в корзине'},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = CartSerializer(
                recipe,
                context={'request': request})
            return Response(serializer.data)

        if self.request.method == 'DELETE':
            if cart:
                cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Рецепта нет в корзине'},
            status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipes, pk=pk)
        chosen = Favorite.objects.filter(user=user, recipe=recipe)
        if self.request.method == "POST":
            if chosen:
                return Response(
                    {'error': 'Рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = CartSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data)

        if self.request.method == 'DELETE':
            if chosen:
                chosen.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Рецепта нет в избранном'},
            status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def download_shopping_cart(self, request, pk=None):
        user = self.request.user
        recipes = Recipes.objects.filter(shopping_cart__user=user)
        if not recipes:
            return Response(status=status.HTTP_204_NO_CONTENT)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.csv"'
        writer = csv.writer(response)
        writer.writerow(['Recipe name', 'Ingredients'])
        for recipe in recipes:
            ingredients = ', '.join([f'{amount} {ingredient.name}' for amount, ingredient in recipe.amount_recipe.all()])
            writer.writerow([recipe.name, ingredients])
        return response
