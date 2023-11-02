from rest_framework import viewsets

from pagination import CustomPagination, IngridientsPagination
from ..recipes.models import (
    Tag,
    Recipe,
    Ingredient,
)
from ..users.models import UserFoodgram
from .serializer import (TagSerializer, UserSerializer)
from .permissions import AuthorStaffOrReadOnly, AdminOrReadOnly


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьювсет для работы с API тегов"""
    queryset = Tag.objects.all()
    pagination_class = CustomPagination
    serializer_class = TagSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """Вьювсет для работы с API юзеров"""
    queryset = UserFoodgram.objects.all()
    pagination_class = [CustomPagination,]
    serializer_class = UserSerializer
    permission_classes = AuthorStaffOrReadOnly


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьювсет для работы с API рецептов"""
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    permission_classes = AuthorStaffOrReadOnly


class IngridientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьювсет для работы с API ингридиентов"""
    queryset = Ingredient.objects.all()
    pagination_class = [IngridientsPagination,]
    permission_classes = AdminOrReadOnly



