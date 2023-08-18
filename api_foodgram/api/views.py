from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from rest_framework import mixins, viewsets, filters, response, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecipeFilter
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    ShoppingCartSerializer,
    TagSerializer
)
from services import ingredients, recipes, tags, users
from users.serializers import CustomUserSerializer, CustomUserCreateSerializer, SubscriptionSerializer
from .permissions import IsAdminOrReadOnly, IsAdminOrAuthorOrReadOnly, IsAuthorOrReadOnly
from recipes.models import Favorite, IngredientInRecipe, Recipe, ShoppingCart


class RetrieveListViewSet(mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    """Создаёт, возвращает объект и список объектов."""

    pass


class IngredientViewSet(RetrieveListViewSet):
    """Обрабатывает ингредиенты и
    делает поиск по названию ингредиента.
    """
    queryset = ingredients.get_all_ingredients()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class TagViewSet(RetrieveListViewSet):
    """Вьюсет для создания тегов."""

    queryset = tags.get_all_tags()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки запросов, связанных с рецептами."""

    queryset = recipes.get_all_recipes()
    # permission_classes = (IsAdminOrAuthorOrReadOnly, IsAuthenticatedOrReadOnly, )
    permission_classes = (IsAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Метод для вызова сериализатора."""

        if self.action in ('list', 'retrieve'):

            return RecipeReadSerializer

        elif self.action in ('create', 'partial_update'):

            return RecipeCreateSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated, ),
        url_path='favorite',
        url_name='favorite'
    )
    def manage_favorite(self, request, pk: int):
        """Метод управления списком избранного."""

        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():

                return Response(
                    {'errors': 'Рецепт уже находится в списке избранного.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            recipe_in_favorite = Favorite.objects.filter(
                user=user,
                recipe=recipe
            )

            if recipe_in_favorite.exists():
                recipe_in_favorite.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(
                {'errors': f'В списке избранного нет рецепта {recipe.name}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated, ),
        url_path='shopping_cart',
        url_name='shopping_cart',
    )
    def shopping_cart(self, request, pk: int):
        """Метод управления списком покупок."""

        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():

                return Response(
                    {'errors': f'Рецепт уже находится в покупок.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = ShoppingCartSerializer(recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            recipe_in_shopping_cart = ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
            )

            if recipe_in_shopping_cart.exists():
                recipe_in_shopping_cart.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(
                {'errors': f'В списке покупок нет рецепта {recipe.name}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def ingredients_to_txt(ingredients: dict) -> str:
        """Метод для объединения всех ингредиентов
        в список покупок для выгрузки.
        """

        shopping_list = ''

        for ingredient in ingredients:
            shopping_list += (
                f"{ingredient['ingredient__name']}  - "
                f"{ingredient['sum']}"
                f"({ingredient['ingredient__measurement_unit']})\n"
            )

        return shopping_list

    @action(
        detail=False,
        permission_classes=(IsAuthenticated, ),
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
    )
    def download_shopping_cart(self, request) -> HttpResponse:
        """Метод для скачивания файла со списком покупок."""

        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by(
                'ingredient__name'
        ).annotate(sum=Sum('amount'))
        shopping_list = self.ingredients_to_txt(ingredients)

        return HttpResponse(shopping_list, content_type='text/plain')


class CustomUserViewSet(UserViewSet):
    """Обрабатывает пользователей."""

    queryset = users.get_all_users()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny, )

    @action(
        methods=['get'],
        detail=False,
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated, )
    )
    def get_me(self, request):
        serializer = CustomUserSerializer(
            request.user,
            context={"request": self.request}
        )

        return Response(serializer.data, status.HTTP_200_OK)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated, ),
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
        permission_classes=(IsAuthenticated, ),
        url_path='subscribe',
        url_name='subscribe',
    )
    def manage_subscriptions(self, request, **kwargs) -> response.Response:
        """Метод управления подписками пользователя (подписка/отписка)."""

        user = request.user
        author_id = self.kwargs.get('id')
        author = users.get_author(author_id)

        if request.method == 'POST':
            serializer = SubscriptionSerializer(author,
                                                data=request.data,
                                                context={'request': request}
                                                )
            serializer.is_valid(raise_exception=True)
            users.create_subscription(user, author)

            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            users.delete_subscription(user, author)

            return response.Response(status=status.HTTP_204_NO_CONTENT)
