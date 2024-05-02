from rest_framework.pagination import PageNumberPagination

class VanuesPageNumberPagination(PageNumberPagination):
    page_size = 5