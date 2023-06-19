from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .pagination import OnDemandResultsPagination
from .serializers import (IngredientsSerializer, RecipesSerializer,
                          TagsSerializer, UserSerializer)
from recipes.models import Ingredients, Recipes, Tags

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = OnDemandResultsPagination


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (filters.SearchFilter,)
    # Поиск по частичному вхождению в начале названия ингредиента.
    search_fields = ('^name',)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = OnDemandResultsPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author', 'tags')
