from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CustomUserViewSet, IngridientsViewSet, RecipesViewSet, TagsViewSet)

app_name = 'api'


router = DefaultRouter()
router.register('users', CustomUserViewSet)
router.register('ingredients', IngridientsViewSet)
router.register('tags', TagsViewSet)
router.register('recipes', RecipesViewSet)



urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]