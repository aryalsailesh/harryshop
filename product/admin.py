from django.contrib import admin
from django import forms
from django.forms import CheckboxSelectMultiple,SelectMultiple
from mptt.admin import MPTTModelAdmin,DraggableMPTTAdmin
from treewidget.fields import TreeManyToManyField,TreeForeignKey
from .models import Checkout,Product,OrderItem,Order,Category

# Register your models here.

admin.site.site_header = 'Admin Dashboard'

class filterCategories(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super(filterCategories,self).__init__(*args,**kwargs)
        self.fields['category'].queryset = Category.objects.filter(children=None)


class ProductAdmin(admin.ModelAdmin):
    
    formfield_overrides = {TreeForeignKey:{'widget':CheckboxSelectMultiple},}
    list_display = ['name','price', 'available','available_quantity', 'created','updated']
    list_filter = ['name','available','created','updated']
    search_fields = ['name','description']
    date_hierarchy = ('created')
    prepopulated_fields = {'slug':('name',)}
    list_editable = ['price','available','available_quantity']

admin.site.register(Product,ProductAdmin)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user','ordered']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','ordered']


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(Category,DraggableMPTTAdmin)