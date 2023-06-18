from rest_framework.pagination import PageNumberPagination


class OnDemandResultsPagination(PageNumberPagination):
    '''Класс для пагинации с определенным пользователем в параметре запроса
    limit количеством объектов на странице.
    '''
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 100
