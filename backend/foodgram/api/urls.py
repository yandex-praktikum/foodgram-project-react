from rest_framework import routers
from django.urls import path, include

from api.views import index, CustomUserViewSet, TagViewSet, RecipeViewSet, IngredientViewSet
from api.views import index, CustomUserViewSet


router = routers.DefaultRouter()
router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('index', index),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls))
]
