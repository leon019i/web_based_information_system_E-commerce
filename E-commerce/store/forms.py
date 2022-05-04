from django.contrib.auth.forms import UserCreationForm

from account.models import Account
from django import forms

class CustomUserForm(UserCreationForm):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter username'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2', 'placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2', 'placeholder':'confirm password'}))
    class Meta:
        model = Account
        fields =['username', 'email', 'password1', 'password2']
    
