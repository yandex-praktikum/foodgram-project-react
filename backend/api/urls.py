from django.urls import include, path
from djoser import views
from rest_framework import routers

from .views import (IngredientsViewSet, RecipesViewSet, TagsViewSet,
                    UsersViewSet)

router = routers.DefaultRouter()
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register('users', UsersViewSet, basename='users')
router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('auth/token/login', views.TokenCreateView.as_view(), name="login"),
    path('auth/token/logout', views.TokenDestroyView.as_view(), name="logout"),
    path('', include(router.urls)),
]
