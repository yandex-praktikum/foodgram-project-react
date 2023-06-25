from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    UsersViewSet, TagViewSet, IngredientViewSet, RecipesList
    )

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('tag', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredients')
# router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('recipes/', RecipesList.as_view()),
]
