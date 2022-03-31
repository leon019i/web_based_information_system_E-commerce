import imp
from multiprocessing import context
import re
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from store.forms import CustomUserForm

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered successfully! Login to continue")
            return redirect('/login')

    context = {'form' : form}
    return render (request, "store/auth/register.html", context)

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('/')

    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=name, password=password) 

            if user is not None:
                login(request, user)
                messages.success(request, "logged in successfully!")

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