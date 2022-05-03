from itertools import product
from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from store.models import Product, Whishlist

def index(request):
    wishlist = Whishlist.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    return render(request,'store/wishlist.html', context)

def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Whishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status':"Product already in wishlist"})
                else:
                    Whishlist.objects.create(user=request.user, product_id = prod_id)
                    return JsonResponse({'status':"Product added to wishlist"})
            else:
                return JsonResponse({'status':"No such product"})
        else:
            return JsonResponse({'status':"Login to continue"})
    return redirect('/')

def deletewishlistitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            
            if(Whishlist.objects.filter(user=request.user, product_id=prod_id)):
                wishlistitem = Whishlist.objects.get(product_id = prod_id, user=request.user)
                wishlistitem.delete()
                return JsonResponse({'status':"Product removed from wishlist"})
            else:
                return JsonResponse({'status':"Product not found in wishlist"})
        else:
            return JsonResponse({'status':"Login to continue"})

    return redirect('/')
