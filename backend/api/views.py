from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import RecipesFilter
from .pagination import OnDemandResultsPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientsSerializer, RecipesGetSerializer,
                          RecipesPostSerializer, TagsSerializer, UserSerializer)
from recipes.models import Ingredients, Recipes, Tags

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = OnDemandResultsPagination

    def get_view_name(self):
        return 'Пользователи'


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (filters.SearchFilter,)
    # Поиск по частичному вхождению в начале названия ингредиента.
    search_fields = ('^name',)

    def get_view_name(self):
        return 'Ингредиенты'


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

    def get_view_name(self):
        return 'Тэги'


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all().select_related()
    serializer_class = RecipesGetSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = OnDemandResultsPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return RecipesGetSerializer
        else:
            return RecipesPostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_view_name(self):
        return 'Рецепты'
