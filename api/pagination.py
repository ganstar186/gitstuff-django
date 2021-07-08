from rest_framework.pagination import PageNumberPagination

class CategoryPostPagination(PageNumberPagination):
    page_size = 8
    page_query_param = 'page'