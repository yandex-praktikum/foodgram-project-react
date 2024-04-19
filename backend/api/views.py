from django.shortcuts import render
from rest_framework import viewsets
from api.serializers import (
    TagSerializer, IngredientSerializer, UserCreateSerializer
)
from recipes.models import (
    Tag, Ingredient, Recipe,
)
from rest_framework import permissions
from api.permissions import ReadOnlyPermission
from api.filters import IngredientFilter
from django_filters.rest_framework import DjangoFilterBackend


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (ReadOnlyPermission,)


class IngredientViewset(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (ReadOnlyPermission,)
    filter_backends = [IngredientFilter,]
    search_fields = ['^name',]


class RecipeVieset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ...
    permission_classes = (permissions.AllowAny,)


class UserViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    # def get_serializer_class(self):
    #     if self.request
    #     return super().get_serializer_class()