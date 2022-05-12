from rest_framework.pagination import LimitOffsetPagination


class MyPagination(LimitOffsetPagination):
    page_size = 6
    page_size_query_param = 'limit'
