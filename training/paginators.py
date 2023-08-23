from rest_framework.pagination import PageNumberPagination

class TrainingPaginator(PageNumberPagination):
    page_size = 10 # количество выводимых объектов на страницу