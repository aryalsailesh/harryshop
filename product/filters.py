import django_filters

from product.models import *

class ProductFilter(django_filters.FilterSet):
    product = django_filters.CharFilter(field_name='name',lookup_expr='icontains')
    class Meta:
        model = Product
        fields = []
        