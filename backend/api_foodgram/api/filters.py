import django_filters

from services import tags
from recipes.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    """ Фильтр списков избранного и покупок."""

    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=tags.get_all_tags(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    is_favorited = django_filters.filters.BooleanFilter(
        method='is_recipe_in_favorited'
    )
    is_in_shopping_cart = django_filters.filters.BooleanFilter(
        method='is_recipe_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def is_recipe_in_favorited(self, queryset, value):
        user = self.request.user

        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)

        return queryset

    def is_recipe_in_shopping_cart(self, queryset, value):
        user = self.request.user

        if value and not user.is_anonymous:
            return queryset.filter(shopping_cart__user=user)

        return queryset
