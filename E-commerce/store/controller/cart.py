from itertools import product
from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Product, Cart

@login_required(login_url='loginpage')
def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id,product_id=prod_id)):
                    return JsonResponse({ 'status':"product already in cart" })
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    if(product_check.quantity >= prod_qty):
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({ 'status':"Product added successfully!" })
                    else:
                        return JsonResponse({ 'status':"Only "+ str(product_check.quantity)+" quantity available"})
            else:
                return JsonResponse({ 'status':"No such product found" })        
        else:
            return JsonResponse({ 'status':"Login to continue" })


    return redirect('/')

@login_required(login_url='loginpage')
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {'cart':cart}
    return render(request, "store/cart.html", context)
@login_required(login_url='loginpage')
def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        product_check = Product.objects.get(id=prod_id)
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get( product_id=prod_id , user=request.user)
            if(product_check.quantity >= prod_qty):
                cart.product_qty = prod_qty
                cart.save()
                return JsonResponse({ 'status':"updated successfully" })
            else:
                return JsonResponse({ 'status':"Only "+ str(product_check.quantity)+" quantity available"})
                

    return redirect('/')
@login_required(login_url='loginpage')
def deleteitem(request):
    if request.method == 'POST':
         prod_id = int(request.POST.get('product_id'))
         if(Cart.objects.filter(user=request.user, product_id=prod_id)):
             cart_item = Cart.objects.get(product_id=prod_id, user=request.user)
             cart_item.delete()
         return JsonResponse({ 'status':"item deleted successfully" })
    
    return redirect('/')



