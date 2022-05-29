from ast import Or
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Order,OrderItem

def index(request):
    orders = Order.objects.filter(user = request.user)
    productnames = OrderItem.objects.raw('SELECT * FROM store_product JOIN store_orderitem ON store_product.id = store_orderitem.product_id JOIN store_order ON store_orderitem.order_id = store_order.id WHERE store_order.user_id = %s ',[request.user.id])
    productnamesarray = []
    productpricesarray = []
    orderstrackingnumberarray = []
    orderdates = []
    status = []
    for x in productnames:
        productnamesarray.append(x.name)
        productpricesarray.append(x.price)
        orderstrackingnumberarray.append(x.tracking_no)
        orderdates.append(x.created_at)
        status.append(x.status)
    # for y in productprices:
    #     productpricesarray.append(y.price)
    zipped = zip(productnamesarray,productpricesarray,orderstrackingnumberarray,orderdates,status)
    context = {'productnamesarray':productnamesarray,'zipped':zipped,'productpricesarray':productpricesarray}
    return render(request,"store/orders/index.html",context)

def vieworder(request, t_no):
    order = Order.objects.filter(tracking_no = t_no).filter(user=request.user).first()
    orderitems= OrderItem.objects.filter(order=order)
    context = {'order':order, 'orderitems':orderitems}
    return render(request, "store/orders/view.html",context)