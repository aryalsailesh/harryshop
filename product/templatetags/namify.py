from django import template
from django.shortcuts import get_object_or_404
from product.models import Category,Order,OrderItem,Product


register = template.Library()

@register.filter
def get_name(value):
    spam = value.split('/')[-1]
    return spam

@register.inclusion_tag('bases.html')
def get_category(category_slug=None):
    category = None
    cats = Category.objects.all()
    cats = cats.filter(parent=None)
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
    return {
        'category':category,
        'cats':cats
        }
    
    
@register.filter
def cart_items(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user,ordered=False)
        if qs.exists():
            counter = qs[0].total_cart_item()
            return counter
    return 0

