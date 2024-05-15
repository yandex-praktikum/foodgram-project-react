import io

from django.db.models import Exists, OuterRef, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (
    Favorites, Follow, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag
)
from users.models import User
from api.filters import RecipeFilter
from api.pagination import Pagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (
    FavoriteRecipeSerializer, FollowCreateSerializer, FollowSerializer, IngredientSerializer,
    FoodgramUserSerializer, RecipeCreateSerializer, ShoppingCartRecipeSerializer,
    RecipeSerializer, TagSerializer
)


class FoodgramUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = FoodgramUserSerializer
    pagination_class = Pagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=self.request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        serializer = FollowCreateSerializer(
            data={'user': user.id, 'following': following.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = FollowSerializer(
            following,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def subscribe_delete(self, request, id):
        user = self.request.user
        following = get_object_or_404(User, id=id)
        follow = Follow.objects.filter(user=user, following=following)
        deleted_count = follow.delete()[0]
        if deleted_count > 0:
            return Response(
                f'Вы отписались от {following}',
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            'Вы не были подписаны на этого пользователя!',
            status=status.HTTP_404_NOT_FOUND
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        return super().me(request)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('^name',)
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if not user.is_anonymous:
            queryset = queryset.annotate(
                is_favorited=Exists(
                    Favorites.objects.filter(
                        user=user, recipe=OuterRef('pk')
                    )
                ),
                is_in_shopping_cart=Exists(
                    ShoppingCart.objects.filter(
                        user=user, recipe=OuterRef('pk')
                    )
                )
            )
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    @staticmethod
    def create_object(request, pk, model, serializer):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response('Такой рецепт уже добавлен',
                            status=status.HTTP_400_BAD_REQUEST)
        data = {'user': user.id, 'recipe': recipe.id}
        serializer = serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @staticmethod
    def delete_object(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        object = model.objects.filter(user=user, recipe=recipe)
        if object.exists():
            object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            'Нельзя удалить то, что не было добавлено',
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk):
        return self.create_object(
            request,
            pk,
            Favorites,
            FavoriteRecipeSerializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_object(request, pk, Favorites)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return self.create_object(
            request,
            pk,
            ShoppingCart,
            ShoppingCartRecipeSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_object(request, pk, ShoppingCart)

    @staticmethod
    def generate_shopping_cart_pdf(ingredients):
        buffer = io.BytesIO()
        pfile = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
        pfile.setFont('DejaVu', 12)
        pfile.drawString(100, 750, 'Список покупок')

        y = 700
        for item in ingredients:
            pfile.drawString(
                100, y,
                f'{item["ingredient__name"]}'
                f'({item["ingredient__measurement_unit"]}) - '
                f'{item["sum"]}'
            )
            y -= 20

        pfile.showPage()
        pfile.save()
        buffer.seek(0)
        return buffer

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shoppingcart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            sum=Sum('amount')
        ).order_by('ingredient__name')
        buffer = self.generate_shopping_cart_pdf(ingredients)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='shopping_cart.pdf'
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
