from cgi import test
import email
import imp
from multiprocessing import context
import re
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from account.models import Account
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from store.forms import CustomUserForm  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.encoding import force_bytes, force_str  

from django.core.mail import EmailMessage  

from store.forms import CustomUserForm
def register(request):
    if request.user.is_authenticated:
        messages.warning(request, "You need to logout before registering a new user")
        return redirect('/')
    else:   
        if request.method == 'POST':
            form = CustomUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)  
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'E-shop password form'  
                message = render_to_string("store/auth/acc_active_email.html", {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':account_activation_token.make_token(user),  
                })
                to_email = form.cleaned_data.get('email')  
                email = EmailMessage(  
                mail_subject, message, to=[to_email]  
                )  
                email.send() 
                messages.success(request, "Please confirm your email address to complete the registration")
                # return redirect('/login')
        else:
            form = CustomUserForm()

    context = {'form' : form}
    return render (request, "store/auth/register.html", context)

def activate(request, uidb64, token):    
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = Account.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token) and (user.is_activated_via_email == False):  
        user.is_active = True 
        user.is_activated_via_email = True 
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.') 
        
    else:
        messages.success(request, "Activation link is invalid!")
        return HttpResponse('Activation link is invalid!')
         
def passwordForm(request, uidb64, token):

    uid = force_str(urlsafe_base64_decode(uidb64))
    user = Account.objects.get(pk=uid)
    if user.is_activated_via_email == False: 
        context = {"uidb64": uidb64, "token":token}
        return render(request, "store/auth/Password_form.html", context)
    else:
        return HttpResponse('Link has already been used!')


def changepassword(request):
    newPassword = request.POST.get('password')
    token = request.POST.get('tok')
    uidb64 = request.POST.get('uidb64')
    if request.method == 'POST':
        try:  
            uid = force_str(urlsafe_base64_decode(uidb64))  
            user = Account.objects.get(pk=uid)  
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):  
            user = None
        if user is not None and account_activation_token.check_token(user, token) and (user.is_activated_via_email == False):
            user.is_active = True 
            user.is_activated_via_email = True 
            user.save()
            user.set_password(newPassword)
            user.save(update_fields=['password'])
            messages.success(request, "Thank you for completing the registeration. Now you can login to your account.")
            return redirect('/login')
        else:
            return HttpResponse('Link has already been used!')

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('/')

    else:
        if request.method == 'POST':
            userEmail = request.POST.get('email')
            password = request.POST.get('password')
            user1 = Account.objects.get(email = userEmail)
            if(not(user1.is_active)):
                messages.error(request, "Your account is suspended, Please contact the system admin!")
                return redirect("/")

            else:
                user = authenticate(request, email=userEmail, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "logged in successfully!")
                    if(user.is_admin):
                        return redirect("/admin")
                    else:
                        return redirect("/")
                else:
                    messages.error(request, "invalid username or password")
                    return redirect("/login")

        return render (request, "store/auth/login.html")


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "logged out successfully!")
    return redirect("/")