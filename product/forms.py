from django import forms
from .models import Checkout,Order
from django.forms import ModelForm



class CheckoutForm(forms.ModelForm):
    
    class Meta:
        model = Checkout
        fields = ['appartment','tol','ward','municipality','district','state']
    
class SearchForm(forms.Form):
    query = forms.CharField()

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['payment']