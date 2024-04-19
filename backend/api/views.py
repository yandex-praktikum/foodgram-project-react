from django.shortcuts import render
from rest_framework import viewsets
from api.serializers import (
    TagSerializer, IngredientSerializer
)
from recipes.models import (
    Tag, Ingredient
)
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