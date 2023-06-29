from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from djoser import utils
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

from .filters import RecipesFilter
from .pagination import OnDemandResultsPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoritesSerializer, IngredientsSerializer,
                          RecipesGetSerializer, RecipesPostSerializer,
                          SetPasswordSerializer, ShoppingCartSerializer,
                          SubscriptionsSerializer, TagsSerializer,
                          UserCreateSerializer, UserGetSerializer)
from recipes.models import (Favorites, Ingredients, Recipes, Shopping_cart,
                            Subscriptions, Tags)

User = get_user_model()


class UsersViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    pagination_class = OnDemandResultsPagination

    def get_serializer_class(self):

        if self.action == "reset_password":
            return SetPasswordSerializer
        if self.request.method == 'POST':
            return UserCreateSerializer

        return self.serializer_class

    @action(
        methods=(SAFE_METHODS),
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=(['post']),
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        utils.logout_user(self.request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_view_name(self):
        return 'Пользователи'


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (filters.SearchFilter,)
    # Поиск по частичному вхождению в начале названия ингредиента.
    search_fields = ('^name',)
    pagination_class = None

    def get_view_name(self):
        return 'Ингредиенты'


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None

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


class SubscriptionsViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_list_or_404(User, following__user=self.request.user)

    def create(self, request, *args, **kwargs):

        user_id = self.kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        if Subscriptions.objects.filter(user=request.user,
                                        following=user).exists():
            data = {"errors": "Подписка уже существует"}
            return Response(data, status=HTTPStatus.BAD_REQUEST)
        Subscriptions.objects.create(
            user=request.user, following=user)
        return Response(status=HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):

        author_id = self.kwargs['users_id']
        user_id = request.user.id

        subscribe = get_object_or_404(
            Subscriptions, user__id=user_id, following__id=author_id)
        subscribe.delete()
        return Response('Подписка удалена', status=HTTPStatus.NO_CONTENT)

    def get_view_name(self):
        return 'Подписка'


class BaseFavoriteShoppingCartViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        try:
            recipe = Recipes.objects.get(id=recipe_id)
            self.model.objects.create(user=request.user, recipe=recipe)
            return Response(status=HTTPStatus.CREATED)
        except (Recipes.DoesNotExist, IntegrityError):
            return Response(status=HTTPStatus.BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        user_id = request.user.id
        try:
            object = self.model.objects.get(
                user__id=user_id, recipe__id=recipe_id)
            object.delete()
        except self.model.DoesNotExist:
            return Response(status=HTTPStatus.BAD_REQUEST)
        return Response(status=HTTPStatus.NO_CONTENT)


class FavoritesViewSet(BaseFavoriteShoppingCartViewSet):
    serializer_class = FavoritesSerializer
    queryset = Favorites.objects.all()
    model = Favorites

    def get_view_name(self):
        return 'В избранное'


class ShoppingCartViewSet(BaseFavoriteShoppingCartViewSet):
    serializer_class = ShoppingCartSerializer
    queryset = Shopping_cart.objects.all()
    model = Shopping_cart

    def get_view_name(self):
        return 'В корзину'
