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
        field_name="tag__slug",
        to_field_name="slug",
        queryset=Tag.objects.all()
    )
    is_favorited = django_filters.BooleanFilter(
        field_name="favorite_recipes", method="filter_favorites"
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        field_name="shopping_cart", method="filter_shopping_cart"
    )

    class Meta:
        model = Recipes
        fields = (
            "tags",
            "author",
        )

    def filter_favorites(self, queryset, name, value):
        return queryset.filter(
            favorite__user=self.request.user
        ) if value else queryset

    def filter_shopping_cart(self, queryset, name, value):
        return (
            queryset.filter(
                shoppingcart__user=self.request.user) if value else queryset
        )
