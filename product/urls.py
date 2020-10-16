from django.urls import path
from django.conf.urls import url
from .views import (
    chekout,
    #ProductListView,
    #ProductDetailView,
    product_detail,
    add_to_cart,
    remove_from_cart,
    CartView,
    add_to_database,
    remove_single_item_from_cart,
    show_category,
    product_list,
    search,
    Esewa,
    EsewaVerify,
    homepage
)



app_name = 'product'

urlpatterns = [
    path('',homepage,name='home'),
    path('esewa-payment/',Esewa.as_view(),name='esewa-request'),
    path('esewa-verify/',EsewaVerify.as_view(),name='esewa-verify'),
    
    path('add-to-database/',add_to_database,name='add-to-database'),
    path('cart/',CartView.as_view(),name='cart'),
    path('product/checkout/',chekout,name='checkout'),
    #path('',ProductListView.as_view(),name='home'),
    path('product/search/',search,name='search'),
    path('products/',product_list,name='products'),
    path('<slug:tag_slug>/',product_list,name='product-tag'),
    path('<slug:category_slug>/',product_list,name='product-category'),
    path('product/<slug:slug>/',product_detail,name='product-detail'),
    #path('product/<slug>/',ProductDetailView.as_view(),name='product-detail'),
    url(r'^product/category/(?P<hierarchy>.+)/$',show_category,name='category'),
    path('add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/',remove_from_cart,name='remove-from-cart'),
    
    
    path('remove-single-item-from-cart/<slug>/',remove_single_item_from_cart,name='remove-single-item-from-cart'),

]