# filters.py (inside your app)
from django_filters import rest_framework as filters
from .models import Book

class BookFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    genre = filters.CharFilter(field_name='genre__name', lookup_expr='icontains')
    condition = filters.CharFilter(field_name='condition__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['author', 'genre', 'condition']

# views.py (update the BookViewSet)

