from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Паджинатор для проекта фудграм"""
    page_size = 6
    page_size_query_param = 'limit'


class IngredientsPagination(PageNumberPagination):
    """Паджинатор для ингридиентов проекта фудграм"""
    page_size = 20
    page_size_query_param = 'limit'

