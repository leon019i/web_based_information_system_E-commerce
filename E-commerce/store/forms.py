from dataclasses import fields
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm

from account.models import Account
from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
from .models import Profile

class CustomUserForm(UserCreationForm):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter username'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter email'}))
    # password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2', 'placeholder':'Enter password'}))
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2', 'placeholder':'Confirm password'}))

    password1 = Account.objects.make_random_password(length=10)
    password2 = password1
    test = password1
    print("this is the password"+test)
    password1 = forms.CharField(initial=password1)
    password2= forms.CharField(initial=password2) 
    captcha = CaptchaField(required=True)
    class Meta:
        model = Account 
        fields =['username', 'email', 'password1', 'password2']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']