from rest_framework import mixins, viewsets, filters, response, status
from rest_framework.decorators import action

from .serializers import IngredientSerializer, RecipeReadSerializer, TagSerializer
from services import ingredients, recipes, tags, users
from users.serializers import CustomUserSerializer, SubscriptionSerializer


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

    @action(
        detail=False,
        # permission_classes=(IsAuthenticated, ),
        url_path='subscriptions',
        url_name='subscriptions',
    )
    def get_subscriptions(self, request):
        """Метод для получения подписок пользователя."""

        queryset = users.get_user_subscriptions(request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(pages,
                                            many=True,
                                            context={'request': request}
                                            )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        # permission_classes=[IsAuthenticated]
        url_path='subscribe',
        url_name='subscribe',
    )
    def manage_subscriptions(self, request) -> response.Response:
        """Метод управления подписками пользователя (подписка/отписка)."""

        user = request.user
        author_id = self.kwargs.get('id')
        author = users.get_author(author_id)

        if request.method == 'POST':
            serializer = SubscriptionSerializer(author,
                                                data=request.data,
                                                context={'request': request})
            serializer.is_valid(raise_exception=True)
            users.create_subscription(user, author)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            users.delete_subscription(user, author)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
