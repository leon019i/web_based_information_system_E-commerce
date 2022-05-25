from itertools import product
from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Product, Whishlist , OrderItem

def index(request):
    wishlist = Whishlist.objects.filter(user=request.user)
    productnames= []
    productordersno = []
    ordersno= []
    count=0
        # for product in trending_products:
        # category = Category.objects.get(id = product.category_id)
        # category_product.append([category, product])
    for prod in wishlist:
        productnames.append(prod.product.name)
        ordersno= Product.objects.raw('SELECT * FROM store_orderitem WHERE store_orderitem.product_id=%s',[prod.product.id])
        for ord in ordersno:
            count =count+1
        productordersno.append(count)
    zipped = zip(wishlist,productordersno)
    context = {'wishlist':wishlist,'productordersno':productordersno, 'zipped' :zipped,'productnames':productnames}
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
