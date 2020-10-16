from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('adminpages/staff_list.html')
def user():
    return {'s_user':User.objects.filter(is_staff=True)}