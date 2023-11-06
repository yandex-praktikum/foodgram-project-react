from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status
from djoser.views import UserViewSet
from rest_framework.response import Response
from recipes.models import (
    Tag, Recipe, Ingredient, ShopCart,
    Favorites, IngredientInRecipe, TagInRecipe
    )
from users.models import UserFoodgram, Fallow

from .permissions import (AuthorOrStaffOrReadOnly,
                          AdminOrReadOnly,
                          IsAuthenticatedOrReadOnlyFoodgram,
                          SAFE_METHODS
                          )
from .paginators import CustomPagination
from .serializers import (
    TagSerializer, IngredientSerializer,
    RecipeReadSerializer, RecipeWriteSerializer, RecipeShortSerializer, CustomUserSerializer, CustomUserCreateSerializer, SubscribeSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import IngredientFilter, RecipeFilter



class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюха дял тегов.
    Через АПИ требуются только GET запросы."""
    queryset = Tag.objects.all()
    permission_classes = [AdminOrReadOnly,]  # имеет ли это поле смысл, ведь ReadOnlyModelViewSet
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюха дял Ingredient.
    В api-спецификации одно, в задание другое,
     в тестах третье... Как работать?"""
    queryset = Ingredient.objects.all()
    permission_classes = [AdminOrReadOnly,]  # имеет ли это поле смысл, ведь ReadOnlyModelViewSet
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


#class RecipesViewSet(viewsets.ModelViewSet):
#    """Вьюха дял Recipe.
#    get, post, patch, del запросы"""
#    queryset = Recipe.objects.all()
#    permission_classes = [AuthorOrStaffOrReadOnly, ]
#    pagination_class = CustomPagination

#    def perform_create(self, serializer):  # !!!!! НАДО ЭТО СПРЯТАТЬ В СЕРИАЛИЗАТОР!
#        """Связываем пост запрос с ег оавтором"""
#        serializer.save(author=self.request.user)

#    def get_serializer_class(self):
#        """Выбираем сериализатор для типов запросов"""
#        if self.request.method in SAFE_METHODS:
#            return RecipeReadSerializer
#        return RecipeWriteSerializer#

#    @action(
#        detail=True,
#        methods=['POST', 'DELETE'],
#        permission_classes=[IsAuthenticatedOrReadOnlyFoodgram]
#    )
#    def favorite(self, request, pk):
#        """Добавить/удалить из избранного."""
#        if request.method == 'POST':
#            return self.add_to(
#                Favorites, request.user, pk
#            )
#        else:
#            return self.delete_from(
#                Favorites, request.user, pk
#            )#

#class TESTRecipeViewSet(viewsets.ModelViewSet):
#    """Вьюсет для модели рецепта."""
#    queryset = Recipe.objects.all()
#    permission_classes = [AuthorOrStaffOrReadOnly]
#    pagination_class = CustomPagination
#    filter_backends = (DjangoFilterBackend,)
#    filterset_class = RecipeFilter
#
#    def perform_create(self, serializer):
#        serializer.save(author=self.request.user)
#
#    def get_serializer_class(self):
#        if self.request.method in SAFE_METHODS:
#            return RecipeReadSerializer
#        return RecipeWriteSerializer
#
#    @action(
#        detail=True,
#        methods=['post', 'delete'],
#        permission_classes=[IsAuthenticatedOrReadOnlyFoodgram]
#    )
#    def favorite(self, request, pk):
#        """Метод для добавления/удаления из избранного."""
#        if request.method == 'POST':
#            return self.add_to(Favorite, request.user, pk)
#        else:
#            return self.delete_from(Favorite, request.user, pk)
#
#    @action(
#        detail=True,
#        methods=['post', 'delete'],
#        permission_classes=[IsAuthenticated]
#    )
#    def shopping_cart(self, request, pk):
#        """Метод для добавления/удаления из списка покупок."""
#        if request.method == 'POST':
#            return self.add_to(ShoppingCart, request.user, pk)
#        else:
#            return self.delete_from(ShoppingCart, request.user, pk)
#
#    def add_to(self, model, user, pk):
#        """Метод для добавления."""
#        if model.objects.filter(user=user, recipe__id=pk).exists():
#            return Response({'errors': 'Рецепт уже добавлен!'},
#                            status=status.HTTP_400_BAD_REQUEST)
#        recipe = get_object_or_404(Recipe, id=pk)
#        model.objects.create(user=user, recipe=recipe)
#        serializer = RecipeShortSerializer(recipe)
#        return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#    def delete_from(self, model, user, pk):
#        """Метод для удаления."""
#        obj = model.objects.filter(user=user, recipe__id=pk)
#        if obj.exists():
#            obj.delete()
#            return Response(status=status.HTTP_204_NO_CONTENT)
#        return Response({'errors': 'Рецепт уже удален!'},
#                        status=status.HTTP_400_BAD_REQUEST)
#
#    @action(
#        detail=False,
#        permission_classes=[IsAuthenticated]
#    )
#    def download_shopping_cart(self, request):
#        """Метод для скачивания списка покупок."""
#        user = request.user
#        if not user.shopping_cart.exists():
#            return Response(status=HTTP_400_BAD_REQUEST)
#        ingredients = IngredientInRecipe.objects.filter(
#            recipe__shopping_cart__user=request.user
#        ).values(
#            'ingredient__name',
#            'ingredient__measurement_unit'
#        ).annotate(amount=Sum('amount'))
#        today = datetime.today()
#        shopping_list = (
#            f'Список покупок для: {user.get_full_name()}\n\n'
#            f'Дата: {today:%Y-%m-%d}\n\n'
#        )
#        shopping_list += '\n'.join([
#            f'- {ingredient["ingredient__name"]} '
#            f'({ingredient["ingredient__measurement_unit"]})'
#            f' - {ingredient["amount"]}'
#            for ingredient in ingredients
#        ])
#        shopping_list += f'\n\nFoodgram ({today:%Y})'
#        filename = f'{user.username}_shopping_list.txt'
#        response = HttpResponse(
#            shopping_list, content_type='text.txt; charset=utf-8'
#        )
#        response['Content-Disposition'] = f'attachment; filename={filename}'
#        return response
#
class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели рецепта."""
    queryset = Recipe.objects.all()
    permission_classes = [AuthorOrStaffOrReadOnly,]
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticatedOrReadOnlyFoodgram]
    )
    def favorite(self, request, pk):
        """Метод для добавления/удаления из избранного."""
        if request.method == 'POST':
            return self.add_to(Favorites, request.user, pk)
        else:
            return self.delete_from(Favorites, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticatedOrReadOnlyFoodgram]
    )
    def shopping_cart(self, request, pk):
        """Метод для добавления/удаления из списка покупок."""
        if request.method == 'POST':
            return self.add_to(ShopCart, request.user, pk)
        else:
            return self.delete_from(ShopCart, request.user, pk)

    def add_to(self, model, user, pk):
        """Метод для добавления."""
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        """Метод для удаления."""
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепт уже удален!'},
                        status=status.HTTP_400_BAD_REQUEST)

class CustomUserViewSet(UserViewSet):
    """Вьюсет для кастомной модели пользователя."""
    queryset = UserFoodgram.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination


    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CustomUserCreateSerializer
        return CustomUserSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticatedOrReadOnlyFoodgram]
    )
    def subscribe(self, request, **kwargs):
        """Метод для подписки/отписки от автора."""
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(UserFoodgram, id=author_id)

        if request.method == 'POST':
            serializer = SubscribeSerializer(author,
                                             data=request.data,
                                             context={'request': request})
            serializer.is_valid(raise_exception=True)
            Fallow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = get_object_or_404(Fallow,
                                             user=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticatedOrReadOnlyFoodgram]
    )
    def subscriptions(self, request):
        """Метод для просмотра подписок на авторов."""
        user = request.user
        queryset = UserFoodgram.objects.filter(follow__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(pages,
                                         many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)
