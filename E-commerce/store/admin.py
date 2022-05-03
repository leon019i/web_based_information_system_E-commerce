from django.contrib import admin

from .models import *
from django.contrib.auth.models import Group

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart) 
admin.site.register(Order) 
admin.site.register(OrderItem) 
admin.site.register(Profile) 
admin.site.unregister(Group)
