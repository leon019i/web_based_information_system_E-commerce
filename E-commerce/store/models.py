from __future__ import unicode_literals
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from numpy import true_divide
from django.conf import settings
#from .managers import UserManager

import email
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

import datetime
import os

# Create your models here.

def get_file_path(request,filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H;%M;%S')
    filename ="%s%s" %(nowTime, original_filename)
    return os.path.join('upload/',filename)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email,user_name, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, user_name,password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,user_name ,password, **extra_fields)

    def create_superuser(self, email,user_name, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email,user_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(_('user name'), max_length=30, blank=True, primary_key=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    avatar = models.ImageField(upload_to='static/upload/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["user_name"]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_user_name(self):
        '''
        Returns the user name.
        ''' 
        return self.user_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Whishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
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
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=150,null=False)
    address=models.TextField(null=False)
    city=models.CharField(max_length=150,null=False)
    state=models.CharField(max_length=150,null=False)
    country=models.CharField(max_length=150,null=False)
    pincode=models.CharField(max_length=150,null=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
