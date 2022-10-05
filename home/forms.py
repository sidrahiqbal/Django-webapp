from django import forms  
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Product


class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'


class JsonForm(forms.Form):
    jsonfile = forms.FileField()
