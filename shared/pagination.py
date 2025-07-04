from rest_framework.pagination import PageNumberPagination

class GlobalPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_strings = ['end']
