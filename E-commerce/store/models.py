from datetime import datetime
import email
from email import contentmanager
from email.policy import default
import imp
import re
from django.db import models
from email import message
from email.mime import image
from statistics import mode
from unicodedata import category
from xmlrpc.client import DateTime
from django.db import models
from django.forms import CharField
from django.core.validators import FileExtensionValidator
# from django.contrib.auth.models import User
from PIL import Image
from account import models as account

import datetime
import os

# Create your models here.

def get_file_path(request,filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H;%M;%S')
    filename ="%s%s" %(nowTime, original_filename)
    return os.path.join('upload/',filename)



class Category(models.Model):
    slug = models.CharField( max_length=150,null=False,blank=False)
    name = models.CharField( max_length=150,null=False,blank=False)
    image = models.ImageField(upload_to=get_file_path, null=True,blank=True)
    description =models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0 = default, 1 = Hidden")
    trending=models.BooleanField(default=False,help_text="0 = default, 1 = Hidden")
    meta_title=models.CharField(max_length=150,null=False,blank=False)
    meta_keywords=models.CharField(max_length=150,null=False,blank=False)
    meta_description =models.TextField(max_length=500,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        
    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug = models.CharField( max_length=150,null=False,blank=False)
    name = models.CharField( max_length=150,null=False,blank=False)
    product_image = models.ImageField(upload_to=get_file_path, null=True,blank=True)
    product_video = models.FileField(upload_to=get_file_path,null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    small_description =models.CharField(max_length=260,null=False,blank=False)
    quantity = models.IntegerField(null=False,blank=False)
    description =models.TextField(max_length=500,null=False,blank=False)
    original_price = models.FloatField(null=False,blank=False)
    selling_price = models.FloatField(null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0 = default, 1 = Hidden")
    trending=models.BooleanField(default=False,help_text="0 = default, 1 = Hidden")
    tag = models.CharField(max_length=150,null=False,blank=False)
    meta_title=models.CharField(max_length=150,null=False,blank=False)
    meta_keywords=models.CharField(max_length=150,null=False,blank=False)
    meta_description =models.TextField(max_length=500,null=False,blank=False)
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(account.Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Whishlist(models.Model):
    user = models.ForeignKey(account.Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user=models.ForeignKey(account.Account,on_delete=models.CASCADE)
    fname=models.CharField(max_length=150,null=False)
    lname=models.CharField(max_length=150,null=False)    
    email=models.CharField(max_length=150,null=False)
    phone=models.CharField(max_length=150,null=False)
    address=models.TextField(null=False)
    city=models.CharField(max_length=150,null=False)
    state=models.CharField(max_length=150,null=False)
    country=models.CharField(max_length=150,null=False)
    pincode=models.CharField(max_length=150,null=False)
    total_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=150,null=False)
    payment_id=models.CharField(max_length=250,null=True)
    orderstatuses=(
    ('Pending','Pending'),
    ('Out For Shipping' ,'Out For Shipping '),
    ('Completed','Completed'),


    )
    status=models.CharField(max_length=150,choices=orderstatuses,default='Pending')
    message=models.TextField(null=True)
    tracking_no=models.CharField(max_length=150,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return '{} - {}'.format(self.id,self.tracking_no)


class OrderItem(models.Model):
        order=models.ForeignKey(Order,on_delete=models.CASCADE)
        product=models.ForeignKey(Product,on_delete=models.CASCADE)    
        price=models.FloatField(null=False)
        quantity=models.IntegerField(null=False)
        
        def __str__(self) :
            return '{} {}' .format(self.order.id,self.order.tracking_no)

class Profile(models.Model):
    user=models.OneToOneField(account.Account,on_delete=models.CASCADE)
    first_name= models.CharField(max_length=150,null=False, default='')
    last_name= models.CharField(max_length=150,null=False, default='')
    profile_image = models.ImageField(upload_to=get_file_path, null=True,blank=True)
    phone=models.CharField(max_length=150,null=False)
    address=models.TextField(null=False)
    city=models.CharField(max_length=150,null=False)
    state=models.CharField(max_length=150,null=False)
    country=models.CharField(max_length=150,null=False)
    pincode=models.CharField(max_length=150,null=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


