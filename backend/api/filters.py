from django_filters import rest_framework

from recipes.models import Recipes


class RecipesFilter(rest_framework.FilterSet):
    is_favorited = rest_framework.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value:
                queryset = queryset.filter(favorite__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value:
                queryset = queryset.filter(purchase__user=user)
        return queryset
    
    class Meta:
        model = Recipes
        fields = ['author', 'is_favorited', 'is_in_shopping_cart', 'tags']
