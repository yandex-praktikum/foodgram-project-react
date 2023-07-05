from api.views import (
    IngredientViewSet,
    RecipesViewSet,
    TagViewSet,
    UsersViewSet
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UsersViewSet, basename="users")
router.register("tags", TagViewSet, basename="tag")
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("recipes", RecipesViewSet, basename="recipes")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
