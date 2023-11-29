from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import RecipesFilter
from api.exceptions import BadRequestException
from api.serializers import (
    IngredientsSerializer,
    RecipesPostSerializer,
    RecipesSerializer,
    TagsSerializer,
    SubscribeSerializer,
    SubscriptionSerializer,
    FavoriteRecipeSerializer,
    ShoppingCartSerializer,
)
from api.viewsets import CreateDestroyViewSet, ListViewSet
# from core.utils import create_shoping_list
from recipes.models import (
    Ingredient,
    ShoppingCart,
    Recipe,
    FavoriteRecipe,
    Tag,
)
from users.models import Subscription

User = get_user_model()


class IngridientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    ordering = ("name",)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    ordering = ("name",)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = (
        Recipe.objects.select_related("author")
        .prefetch_related("tags", "ingredients_recipes")
        .all()
    )
    serializer_class = RecipesSerializer
    filterset_class = RecipesFilter
    ordering = ("-pub_date",)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user)
        
    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return RecipesPostSerializer
        return RecipesSerializer

    @action(
        detail=False,
        methods=('get',),
        url_path='download_shopping_cart',
        pagination_class=None)
    def download_file(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(
                'В корзине нет товаров', status=status.HTTP_400_BAD_REQUEST)

        text = 'Список покупок:\n\n'
        ingredient_name = 'recipe__recipe__ingredient__name'
        ingredient_unit = 'recipe__recipe__ingredient__measurement_unit'
        recipe_amount = 'recipe__recipe__amount'
        amount_sum = 'recipe__recipe__amount__sum'
        cart = user.shopping_cart.select_related('recipe').values(
            ingredient_name, ingredient_unit).annotate(Sum(
                recipe_amount)).order_by(ingredient_name)
        for _ in cart:
            text += (
                f'{_[ingredient_name]} ({_[ingredient_unit]})'
                f' — {_[amount_sum]}\n'
            )
        response = HttpResponse(text, content_type='text/plain')
        filename = 'shopping_list.txt'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    """
    @action(methods=["get"], detail=False)
    def download_shopping_cart(self, request):
        user = self.request.user
        shopping_list = create_shoping_list(user)
        return shopping_list
    """


class SubscriptionsViewSet(ListViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ("author",)

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            id__in=user.subscriber.values("author_id")).annotate(
            recipes_count=Count("recipes")
        )


class SubscribeViewSet(CreateDestroyViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        author = get_object_or_404(User, pk=self.kwargs["id"])
        subscriber = self.request.user
        return get_object_or_404(queryset, subscriber=subscriber,
                                 author=author)

    def perform_create(self, serializer):
        author = get_object_or_404(User, pk=self.kwargs["id"])
        serializer.save(subscriber=self.request.user, author=author)



class FavoriteRecipeViewSet(CreateDestroyViewSet):
    serializer_class = FavoriteRecipeSerializer

    def get_queryset(self):
        user = self.request.user.id
        return FavoriteRecipe.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            favorite_recipe=get_object_or_404(
                Recipe,
                id=self.kwargs.get('recipe_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        u = request.user
        if not u.favorite.select_related(
                'favorite_recipe').filter(
                    favorite_recipe_id=recipe_id).exists():
            return Response({'errors': 'Рецепт не в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(
            FavoriteRecipe,
            user=request.user,
            favorite_recipe_id=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(CreateDestroyViewSet):
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        user = self.request.user.id
        return ShoppingCart.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(
                Recipe,
                id=self.kwargs.get('recipe_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        u = request.user
        if not u.shopping_cart.select_related(
                'recipe').filter(
                    recipe_id=recipe_id).exists():
            return Response({'errors': 'Рецепта нет в корзине'},
                            status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(
            ShoppingCart,
            user=request.user,
            recipe=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
