import django_filters
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
    is_favorited = django_filters.BooleanFilter(
        field_name="favorite_recipes__user",
        method="filter_favorites",
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        field_name="shopping_cart", method="filter_shopping_cart"
    )

    class Meta:
        model = Recipes
        fields = (
            "is_favorited",
            "tags",
            "author",
        )

    def filter_favorites(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(favorite_recipes__user=user)
        return queryset.exclude(favorite_recipes__user=user)

    def filter_shopping_cart(self, queryset, name, value):
        return (
            queryset.filter(
                shoppingcart__user=self.request.user) if value else queryset
        )
