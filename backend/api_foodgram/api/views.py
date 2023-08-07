from rest_framework import mixins, viewsets, filters

from .serializers import IngredientSerializer, RecipeReadSerializer, TagSerializer
from services import ingredients, recipes, tags, users
from users.serializers import CustomUserSerializer


class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    """Создаёт, возвращает объект и список объектов.
    """

    pass


class IngredientViewSet(CreateRetrieveListViewSet):
    """Обрабатывает ингредиенты и
    делает поиск по названию ингредиента.
    """
    queryset = ingredients.get_all_ingredients()
    serializer_class = IngredientSerializer
    # permission_classes
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # Вернуть ответ в виде файла, а не текстового списка


class TagViewSet(CreateRetrieveListViewSet):
    """Вьюсет для создания тегов."""

    queryset = tags.get_all_tags()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки запросов, связанных с рецептами."""

    queryset = recipes.get_all_recipes()
    serializer_class = RecipeReadSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """Обрабатывает пользователей."""

    queryset = users.get_all_users()
    serializer_class = CustomUserSerializer
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('username',)
    # lookup_field = 'username'
