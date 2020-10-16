"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from account.views import (
    admin_login,
    admin_home,
    admin_order_detail,
    user_list,
    user_detail
)

urlpatterns = [
    path('admin-login/',admin_login,name='admin-login'),
    path('admin-home/',admin_home,name='admin-home'),
    path('admin-order-detail/<int:id>/',admin_order_detail,name='order-detail'),
    path('admin-list/users/',user_list,name='user-list'),
    path('admin-list/users/<int:id>/',user_detail,name='user-detail'),
    path('admin/', admin.site.urls),
    path(
    'admin/password_reset/',
    auth_views.PasswordResetView.as_view(),
    name='admin_password_reset',),
    path('treewidget/', include('treewidget.urls')),
    path('account/',include('account.urls')),
    path('social-auth/',include('social_django.urls',namespace='social')),
    path('',include('product.urls',namespace='product')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                            document_root=settings.STATIC_ROOT)