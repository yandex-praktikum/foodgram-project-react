from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.serializers import (
    IngredientsSerializer,
    RecipesPostSerializer,
    RecipesSerializer,
    TagsSerializer,
    SubscribeSerializer,
    SubscriptionSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
)
from api.viewsets import CreateDestroyViewSet, ListViewSet
from core.utils import create_shoping_list
from recipes.models import (
    Ingredient,
    ShoppingCart,
    IngredientRecipe,
    Recipe,
    Tag,
    Favorite,
)
from users.models import Subscription

User = get_user_model()


class IngridientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    ordering = ("name",)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    ordering = ("name",)


class RecipesViewSet(viewsets.ModelViewSet):  # , CustomSerializerContext
    queryset = (
        Recipe.objects.select_related("author")
        .prefetch_related("tags", "ingredients_recipes")
        .all()
    )
    serializer_class = RecipesSerializer
    ordering = ("-pub_date",)

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return RecipesPostSerializer
        return RecipesSerializer

    @action(methods=["get"], detail=False)
    def download_shopping_cart(self, request):
        user = self.request.user
        shopping_list = create_shoping_list(user)
        return shopping_list


class SubscriptionsViewSet(ListViewSet):  # , CustomSerializerContext
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ("author",)

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            id__in=user.subscriber.values("author_id")).annotate(
            recipes_count=Count("recipes")
        )


class SubscribeViewSet(CreateDestroyViewSet): # , CustomSerializerContext
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        author = get_object_or_404(User, pk=self.kwargs["id"])
        subscriber = self.request.user
        return get_object_or_404(queryset, subscriber=subscriber,
                                 author=author)

    def perform_create(self, serializer):
        author = get_object_or_404(User, pk=self.kwargs["id"])
        serializer.save(subscriber=self.request.user, author=author)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        recipe = get_object_or_404(Recipe, pk=self.kwargs["id"])
        user = self.request.user
        return get_object_or_404(queryset, recipe=recipe, user=user)

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["id"])
        serializer.save(user=self.request.user, recipe=recipe)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        recipe = get_object_or_404(Recipe, pk=self.kwargs["id"])
        user = self.request.user
        return get_object_or_404(queryset, recipe=recipe, user=user)

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["id"])
        serializer.save(user=self.request.user, recipe=recipe)
