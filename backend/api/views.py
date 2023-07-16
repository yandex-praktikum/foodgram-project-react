from datetime import datetime
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse

from djoser import utils
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

from .filters import RecipesFilter
from .pagination import OnDemandResultsPagination
from .permissions import IsAuthorOrReadOnly, IsAuthenticatedOrPostOnly
from .serializers import (CollectionSerializer, IngredientsSerializer,
                          RecipesGetSerializer, RecipesMinifieldSerializer,
                          RecipesPostSerializer, RecipesShortSerializer,
                          SetPasswordSerializer, SubscriptionsSerializer,
                          TagsSerializer, UserCreateSerializer,
                          UserGetSerializer)
from recipes.models import (Favorites, Ingredients, Recipes, RecipeIngredient,
                            Shopping_cart, Subscriptions, Tags)

User = get_user_model()


class UsersViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    pagination_class = OnDemandResultsPagination
    permission_classes = (IsAuthenticatedOrPostOnly,)

    def get_serializer_class(self):

        if self.action == "set_password":
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
    def set_password(self, request):
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
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = OnDemandResultsPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter

    def get_serializer_class(self):

        if self.request.method in SAFE_METHODS:
            return RecipesGetSerializer
        else:
            return RecipesPostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_to_collection(self, model, user, recipe__id):
        if model.objects.filter(user=user, recipe__id=recipe__id).exists():
            return Response({'errors': 'Рецепт уже добавлен'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipes, id=recipe__id)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipesShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from_collection(self, model, user, recipe__id):
        obj = model.objects.filter(user=user, recipe__id=recipe__id)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепт уже удален'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to_collection(Favorites, request.user, pk)
        else:
            return self.delete_from_collection(Favorites, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to_collection(Shopping_cart, request.user, pk)
        else:
            return self.delete_from_collection(Shopping_cart, request.user, pk)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.buyer.all().exists():
            return Response(
                {'errors': 'Корзина пуста'},
                status=HTTPStatus.BAD_REQUEST
            )

        ingredients = RecipeIngredient.objects.filter(
            recipe__purchase__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        today = datetime.today()
        shopping_list = (
            f'Список покупок для: {user.get_full_name()}\n\n'
            f'Дата: {today:%Y-%m-%d}\n\n'
        )
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        shopping_list += f'\n\nFoodgram ({today:%Y})'

        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response

    def get_view_name(self):
        return 'Рецепты'


class SubscriptionsViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = OnDemandResultsPagination

    def get_queryset(self):
        return get_list_or_404(User, following__user=self.request.user)

    def check_subscriptions(self, user_id, following_id):
        following = get_object_or_404(User, id=following_id)
        return (following,
                Subscriptions.objects.filter(user=user_id,
                                             following=following_id).first())

    def create(self, request, *args, **kwargs):

        author_id = self.kwargs['users_id']
        user_id = request.user.id

        following, subscribe = self.check_subscriptions(user_id, author_id)

        if subscribe:
            data = {"errors": "Подписка уже существует"}
            return Response(data, status=HTTPStatus.BAD_REQUEST)
        Subscriptions.objects.create(
            user=request.user, following=following)

        new_queryset = Recipes.objects.filter(author=author_id)
        serializer = RecipesMinifieldSerializer(new_queryset,
                                                context={'request': request},
                                                many=True,)

        return Response(serializer.data, status=HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):

        author_id = self.kwargs['users_id']
        user_id = request.user.id

        _, subscribe = self.check_subscriptions(user_id, author_id)

        if subscribe:
            subscribe.delete()
            return Response('Подписка удалена', status=HTTPStatus.NO_CONTENT)

        data = {"errors": "Подписка не существует"}
        return Response(data, status=HTTPStatus.BAD_REQUEST)

    def get_view_name(self):
        return 'Подписка'
