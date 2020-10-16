import django_filters
from django_filters import CharFilter
from django.contrib.auth.models import User 
from .models import Profile

from product.models import *

class OrderItemFilter(django_filters.FilterSet):
    
    class Meta:
        model = OrderItem
        fields = ['user','ordered','payment']


class UserFilter(django_filters.FilterSet):
   
    username = CharFilter(field_name='username',lookup_expr='icontains')
    class Meta:
        model = User
        fields  = ['is_staff']