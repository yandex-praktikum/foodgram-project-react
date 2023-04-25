from django.urls import include, path

from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                       UserFoodgramViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'users', UserFoodgramViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
