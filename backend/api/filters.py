from django_filters import rest_framework as filters
from recipes.models import Ingredient, Recipes, Tag


class IngredientsFilter(filters.FilterSet):
    """Фильтры для Ингридиентов."""

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipesFilter(filters.FilterSet):
    """Фильтры для Рецептов."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        field_name="in_favorite__author",
        method="filter_favorites",
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name="shopping_cart_user",
        method="filter_shopping_cart"
    )

    class Meta:
        model = Recipes
        fields = (
            "tags",
            "author",
            "is_favorited",
            'is_in_shopping_cart',
        )

    def filter_favorites(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(in_favorite__user=user)
        return queryset.exclude(in_favorite__user=user)

    def filter_shopping_cart(self, queryset, name, value):
        return (
            queryset.filter(
                shopping_cart_user=self.request.user) if value else queryset
        )
