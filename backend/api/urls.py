from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    TagViewset, IngredientViewset, UserViewset
)


app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewset, 'tags')
router.register('ingredients', IngredientViewset, 'ingredients')
router.register('users', UserViewset, 'users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]