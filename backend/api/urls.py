import djoser.urls.authtoken
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from views import (TagsViewSet, UsersViewSet, RecipesViewSet, IngridientsViewSet)

app_name = 'api'

router = DefaultRouter()

router.register(prefix='tags', viewset=TagsViewSet)
router.register(prefix='users', viewset=UsersViewSet)
router.register(prefix='recipes', viewset=RecipesViewSet)
router.register(prefix='ingridients', viewset=IngridientsViewSet)

urlpatterns = (
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
)
