import django_filters
from recipes.models import Ingredient
from rest_framework.filters import SearchFilter



class IngredientFilter(SearchFilter):
    search_param = 'name'