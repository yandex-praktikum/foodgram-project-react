from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                       UserFoodgramViewSet)

v1_router = DefaultRouter()
v1_router.register(
    r'ingredients', IngredientViewSet, basename='ingredients')
v1_router.register(r'tags', TagViewSet, basename='tags')
v1_router.register(r'recipes', RecipeViewSet, basename='recipes')
v1_router.register(r'users', UserFoodgramViewSet, basename='users')

urlpatterns = [
    path('', include(v1_router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
