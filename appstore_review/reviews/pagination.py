from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # 기본 페이지 크기
    page_size_query_param = 'page_size'  # 클라이언트가 페이지 크기 지정 가능 (예: ?page_size=20)
    max_page_size = 100  # 최대 페이지 크기 제한
