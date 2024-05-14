from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(
        method='is_recipe_in_favorites_filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_recipe_in_shoppingcart_filter'
    )

    def is_recipe_in_favorites_filter(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            user = self.request.user
            return queryset.filter(favorites__user_id=user.id)
        return queryset

    def is_recipe_in_shoppingcart_filter(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            user = self.request.user
            return queryset.filter(shoppingcart__user_id=user.id)
        return queryset

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']
