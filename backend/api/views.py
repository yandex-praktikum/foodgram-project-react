import csv

from api.filters import IngredientsFilter, RecipesFilter
from api.pagination import PageLimitPagination
from api.serializers import (
    CartSerializer,
    CustomUserSerializer,
    IngredientSerilizer,
    RecipesPostUpdateSerializer,
    RecipesSerializer,
    SubscribeSerializer,
    TagSerializer,
)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from djoser.views import UserViewSet
from foodgram.settings import SHOPCART_FILENAME
from recipes.models import Favorite, Ingredient, Recipes, ShoppingCart, Tag
from users.models import Subscribe, User

TEXT_CSV = "text/csv"


class UsersViewSet(UserViewSet):
    """Вьюсет для получения информации о пользователях."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    search_fields = ("username", "email")
    permission_classes = (AllowAny,)
    pagination_class = PageLimitPagination

    @action(
        methods=("GET",),
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        serializer = SubscribeSerializer(user, context={"request": request})
        return Response(serializer.data)

    @action(
        methods=(
            "POST",
            "DELETE",
        ),
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id):
        user = self.request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                {"error": "Нельзя подписатся на себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscribers = Subscribe.objects.filter(
            user=user,
            author=author
        )
        if self.request.method == "POST":
            if subscribers.exists():
                return Response(
                    {"error": "Уже подписан"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Subscribe.objects.create(user=request.user, author=author),
            serializer = SubscribeSerializer(
                author, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if self.request.method == "DELETE":
            if subscribers.exists():
                subscribers.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Такой подписки нет"}, status=status.HTTP_400_BAD_REQUEST
        )


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет создания тегов"""

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
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = IngredientsFilter
    search_fields = ("name",)

    @action(detail=False)
    def get_ingredients(self, request):
        ingredient = Ingredient.objects.all()
        serializer = self.get_serializer(ingredient, many=True)
        return Response(serializer.data)


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания рецептов"""

    queryset = Recipes.objects.all().order_by("id")
    permission_classes = (AllowAny,)
    pagination_class = PageLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipesSerializer
        return RecipesPostUpdateSerializer

    @action(detail=False, methods=("get",))
    def get_recipes(self, request):
        recipes = Recipes.objects.all()
        serializer = RecipesSerializer(recipes, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=(
            "post",
            "patch",
            "delete",
        ),
        permission_classes=(IsAuthenticated,),
    )
    def post_recipes(self, request):
        serializer = RecipesPostUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=True,
        methods=(
            "post",
            "delete",
        ),
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipes, pk=pk)
        cart = ShoppingCart.objects.filter(user=user, recipe=recipe)

        if self.request.method == "POST":
            if cart.exists():
                return Response(
                    {"error": "Рецепт уже в корзине"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = CartSerializer(recipe, context={"request": request})
            return Response(serializer.data)

        if self.request.method == "DELETE":
            if cart.exists():
                cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Рецепта нет в корзине"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=(
            "post",
            "delete",
        ),
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipes, pk=pk)
        chosen = Favorite.objects.filter(user=user, recipe=recipe)
        if self.request.method == "POST":
            if chosen.exists():
                return Response(
                    {"error": "Рецепт уже в избранном"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = CartSerializer(recipe, context={"request": request})
            return Response(serializer.data)

        if self.request.method == "DELETE":
            if chosen.exists():
                chosen.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Рецепта нет в избранном"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=("get",),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request, pk=None):
        user = self.request.user
        recipes = Recipes.objects.filter(shopping_cart__user=user)
        if not recipes:
            return Response(status=status.HTTP_204_NO_CONTENT)
        response = HttpResponse(content_type=TEXT_CSV)
        response["Content-Disposition"] = "attachment; filename=" + \
            SHOPCART_FILENAME
        writer = csv.writer(response)
        writer.writerow(
            (
                "Recipe name",
                "Ingredients",
            )
        )
        for recipe in recipes:
            ingredients = ", ".join(
                [
                    f"{amount} {ingredient.name}"
                    for amount, ingredient in recipe.amount_recipe.all()
                ]
            )
            writer.writerow(
                (
                    recipe.name,
                    ingredients,
                )
            )
        return response
