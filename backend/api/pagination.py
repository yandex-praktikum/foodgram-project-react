from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Настраивает пагинацию в соответствии с
    /?page=<integer>&limit=<integer>"""

    page_size = 6
    page_query_param = "page"
    page_size_query_param = "limit"
    page_query_description = "Номер страницы."
    page_size_query_description = "Количество объектов на странице."
