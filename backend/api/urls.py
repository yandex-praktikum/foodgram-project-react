from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    TagViewset, IngredientViewset,
)


app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewset, 'tags')
router.register('ingredients', IngredientViewset, 'ingredients')

urlpatterns = [
    path('', include(router.urls)),
]