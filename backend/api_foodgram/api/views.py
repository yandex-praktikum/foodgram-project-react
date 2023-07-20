from rest_framework import mixins, viewsets, filters

from .serializers import IngredientSerializer, TagSerializer
from services import ingredients, tags


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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # Вернуть ответ в виде файла, а не текстового списка


class TagViewSet(CreateRetrieveListViewSet):
    """Обрабатывает теги.
    """
    queryset = tags.get_all_tags()
    serializer_class = TagSerializer


class RecipeViewSet():
    pass
