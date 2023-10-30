from rest_framework.pagination import PageNumberPagination


class FoodPagination(PageNumberPagination):
    '''Паджинатор для проекта фудграм'''
    page_size = 6
    page_size_query_param = 'limit'
