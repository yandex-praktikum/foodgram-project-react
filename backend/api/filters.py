from django_filters import rest_framework

from recipes.models import Recipes


class RecipesFilter(rest_framework.FilterSet):
    IN_SHOPPING_CART_CHOICES = (
        (1, 'In shopping cart'),
        (0, 'Not in shopping cart'),
    )

    IS_FAVORITES_CHOICES = (
        (1, 'Is favorites'),
        (0, 'Not is favorites'),
    )

    is_favorited = rest_framework.ChoiceFilter(
        choices=IS_FAVORITES_CHOICES,
        method='filter_is_favorited',
        label='Is Favorited'
    )
    is_in_shopping_cart = rest_framework.ChoiceFilter(
        choices=IN_SHOPPING_CART_CHOICES,
        method='filter_is_in_shopping_cart',
        label='Is in shopping cart'
    )

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value == 1:
                queryset = queryset.filter(favorite__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value == 1:
                queryset = queryset.filter(purchase__user=user)
        return queryset
    
    class Meta:
        model = Recipes
        fields = ['author', 'is_favorited', 'is_in_shopping_cart', 'tags']
