from django.contrib.auth.forms import UserCreationForm

from account.models import Account
from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput

class CustomUserForm(UserCreationForm):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter username'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2', 'placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2', 'placeholder':'Confirm password'}))
    captcha = CaptchaField(required=True,widget=CaptchaTextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter captcha'}))
    class Meta:
        model = Account 
        fields =['username', 'email', 'password1', 'password2']
    
