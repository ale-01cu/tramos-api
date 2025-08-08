from rest_framework.pagination import CursorPagination

class PaginationCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'  # Campo para ordenar
    cursor_query_param = 'cursor'