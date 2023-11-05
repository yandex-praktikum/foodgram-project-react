from rest_framework import viewsets
from rest_framework.decorators import action



from recipes.models import (
    Tag, Recipe, Ingredient, ShopCart,
    Favorites, IngredientInRecipe, TagInRecipe
    )
from users.models import UserFoodgram, Fallow

from .permissions import (AuthorStaffOrReadOnly,
                          AdminOrReadOnly,
                          IsAuthenticatedOrReadOnlyFoodgram,
                          SAFE_METHODS
                          )
from .pagination import CustomPagination
from .serializer import TagSerializer, IngredientSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import IngredientFilter


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюха дял тегов"""
    queryset = Tag.objects.all()
    permission_classes = [AdminOrReadOnly,]
    serializer_class = TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюха дял Recipe"""
    queryset = Recipe.objects.all()
    permission_classes = [AuthorStaffOrReadOnly,]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Связываем пост запрос с ег оавтором"""
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Выбираем сериализатор для типов запросов"""
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnlyFoodgram]
    )
    def favorite(self, request, pk):
        """Добавить/удалить из избранного."""
        if request.method == 'POST':
            return self.add_to(
                Favorites, request.user, pk
            )
        else:
            return self.delete_from(
                Favorites, request.user, pk
            )


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюха дял Ingredient"""
    queryset = Ingredient.objects.all()
    permission_classes = [AdminOrReadOnly,]
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class UserFoodgramViewSet(viewsets.ModelViewSet):
    """Вьюха дял UserFoodgram"""
    queryset = UserFoodgram.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """Выбираем сериализатор для типов запросов"""
        pass



class ShopCartViewSet(viewsets.ModelViewSet):
    """Вьюха дял ShopCart"""
    queryset = ShopCart.objects.all()


class IngredientInRecipeViewSet(viewsets.ModelViewSet):
    """Вьюха дял IngredientInRecipe"""
    queryset = IngredientInRecipe.objects.all()


class FavoritesViewSet(viewsets.ModelViewSet):
    """Вьюха дял Favorites"""
    queryset = Favorites.objects.all()


class TagInRecipeViewSet(viewsets.ModelViewSet):
    """Вьюха дял TagInRecipe"""
    queryset = TagInRecipe.objects.all()


class FallowViewSet(viewsets.ModelViewSet):
    """Вьюха дял Fallow"""
    queryset = Fallow.objects.all()

