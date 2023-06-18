from django.urls import include, path
from rest_framework import routers

from .views import IngredientsViewSet, TagsViewSet, UsersViewSet

router = routers.DefaultRouter()
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
