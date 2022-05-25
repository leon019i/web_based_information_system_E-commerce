from asyncio import events
from email import message
import email
from itertools import product
import json
from multiprocessing import context
from pyexpat.errors import messages
from unicodedata import category
from urllib import request
from xmlrpc.client import DateTime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from pymysql import Date
from tomlkit import datetime
from account.models import Account
from .models import Category, Order, OrderItem,  Product , Cart
# Create your views here.


def home(request):
    category_product = []
    trending_products = Product.objects.filter(trending=1)
    for product in trending_products:
        category = Category.objects.get(id = product.category_id)
        category_product.append([category, product])

    
    
    context = {
        'category_product': category_product,
        'trending_products' : trending_products
        }
    print(category_product)
    return render(request, "store/index.html",context)


def collections(request):
    category = Category.objects.filter(status=0)
    categorynames=[]
    catprod1=[]
    catprod2=[]
    catprod3=[]
    catprod4=[]
    number=0
    numberofproductsincat = []
    allproducts = Product.objects.all()
    for cat in category:
        categorynames.append(cat.name)

    for prod in allproducts:
        if prod.category.name =="Fashion":
            catprod1.append(prod.name)
        elif prod.category.name=="Footware":
            catprod2.append(prod.name)

        elif prod.category.name == "Mobiles":
            catprod3.append(prod.name)

        else:
            catprod4.append(prod.name)
    
    number = len(catprod1)
    numberofproductsincat.append(number)

    number = len(catprod2)

    numberofproductsincat.append(number)
    
    number = len(catprod3)

    numberofproductsincat.append(number)
    
    number = len(catprod4)

    numberofproductsincat.append(number)
    
    zipped = zip(category,numberofproductsincat)
    context = {'category': category,'zipped': zipped ,'numberofproductsincat':numberofproductsincat,'categorynames':categorynames}
    return render(request, "store/collections.html", context)


def collectionsview(request, slug):
    if(Category.objects.filter(slug=slug, status=0)):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {'products': products, 'category': category}
        return render(request, "store/products/index.html", context)
    else:
        messages.warning(request, "No such category found")
        return redirect('collections')


def productview(request, cate_slug, prod_slug):
    if(Category.objects.filter(slug=cate_slug, status=0)):
        if(Product.objects.filter(slug=prod_slug, status=0)):
            products = Product.objects.filter(slug=prod_slug, status=0).first
            context = {'products': products}
        else:
            # return HttpResponse("no product found")
            return redirect('collections')

    else:
        messages.warning(request, "No such category found")
        return redirect('collections')
        
    return render(request, "store/products/view.html", context)

def productlistAjax(request):
    products = Product.objects.filter(status=0).values_list('name',flat=True)
    productsList = list(products)
    return JsonResponse(productsList,safe=False)

def searchproduct(request):
    if request.method =='POST':
        searchedterm = request.POST.get('productsearch')
        if searchedterm =="":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__icontains=searchedterm).first()
            if product:
                return redirect('collections/'+product.category.slug+'/'+product.slug)
            else:
                return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))

def forget_password(request):
    return render(request, "store/auth/forget_password.html")


def forget_password_first(request):
    if request.method == 'POST':
        useremail = request.POST['fp_email']
        print(useremail)
        u = Account.objects.get(email =useremail)
        user_new_password = Account.objects.make_random_password(length=10)
        print(user_new_password)
        u.set_password(user_new_password)
        u.save(update_fields=['password'])
        name =  Account.objects.get(email =useremail).username
        subject = useremail +' password reset'
        message =  "Hi "+ name + ",\n"+"There was a request to change your password!\n"+"If you did not make this request then please ignore this email.\n"+"Here's your email: "+useremail+"\n"+"Here's your password: "+user_new_password

        send_mail(subject=subject,message=message,from_email='lordleo68@gmail.com' ,recipient_list=["leonlord0@gmail.com",useremail])

        return render(request, "store/auth/after_reset_pass.html")




# def adminchart1(request):
#     #top places/cities that sold products
#     numberofcairo = 0
#     numberofgiza = 0
#     ordersincairo = Order.objects.raw('SELECT COUNT(store_order.city) FROM store_order WHERE store_order.city= %s ',['cairo'])
#     ordersingiza = Order.objects.raw('SELECT COUNT(store_order.city) FROM store_order WHERE store_order.city= %s ',['giza'])
#     for x in ordersincairo:
#         numberofcairo = numberofcairo+1
#     for y in ordersingiza:
#         numberofgiza = numberofgiza+1
#     context = {'numberofcairo': numberofcairo,'numberofgiza': numberofgiza}
#     return(request,"env/Lib/site-packages/jazzmin/templates/admin/base.html", context)

