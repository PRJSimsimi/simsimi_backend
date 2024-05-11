import django_filters
from .models import customer_reviews

class ReviewFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_date', lookup_expr='lte')
    rating = django_filters.NumberFilter(field_name='rating')
    territory = django_filters.CharFilter(field_name='territory')

    class Meta:
        model = customer_reviews
        fields = ['rating', 'start_date', 'end_date', 'territory']
