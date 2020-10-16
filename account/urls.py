from django.urls import path,include
from django.conf.urls import url
from .views import dashbord,register,edit,activate,contact,a_edit
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('profile/',dashbord,name='dashboard'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    
    path('',include('django.contrib.auth.urls'),{'redirect_if_logged_in': '/'}),
    path('address/',a_edit,name='address'),
    path('contact/',contact,name='contact'),
    path('register/',register,name='register'),
    path('edit/',edit,name='edit'),
    
    
]