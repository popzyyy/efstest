from django import forms
from .models import *

from .models import Customer, Stock, Investment, Fund, Mutual,User
from django.contrib.auth.forms import UserCreationForm

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('cust_number', 'name', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone',)
class StockForm(forms.ModelForm):
   class Meta:
       model = Stock
       fields = ('customer', 'symbol', 'name', 'shares', 'purchase_price', 'purchase_date',)

class InvestmentForm(forms.ModelForm):
   class Meta:
       model = Investment
       fields = ('customer', 'category', 'description', 'acquired_value', 'acquired_date', 'recent_value', 'recent_date',)

class FundForm(forms.ModelForm):
   class Meta:
       model = Fund
       fields = ('customer', 'type', 'description', 'minimum_purchase', 'purchase_date', 'purchase_value', 'recent_date','present_value',)

class MutualForm(forms.ModelForm):
   class Meta:
       model = Mutual
       fields = ('customer', 'name', 'shares', 'recent_date', 'purchase_value', 'recent_date','present_value',)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)
    username = forms.CharField(min_length=3, max_length=30, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Again', widget=forms.PasswordInput)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer.pk')
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]