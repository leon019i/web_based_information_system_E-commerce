from django.contrib import admin

from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from account.models import Account

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)

admin.site.register(Cart) 
admin.site.register(Order) 
admin.site.register(OrderItem) 
admin.site.register(Profile) 

admin.site.unregister(Group)

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff','is_activated_via_email')
    search_fields = ('email', 'username')
    readonly_fields=('date_joined', 'last_login', 'is_activated_via_email')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    def changelist_view(self, request, extra_context=None):
        ordersincairo = Order.objects.raw('SELECT COUNT(store_order.city) FROM store_order WHERE store_order.city= %s ',['cairo'])
        ordersingiza = Order.objects.raw('SELECT COUNT(store_order.city) FROM store_order WHERE store_order.city= %s ',['giza'])
        extra_context = extra_context or {"ordersincairo" :ordersincairo,"ordersingiza":ordersingiza}
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Account, AccountAdmin)

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