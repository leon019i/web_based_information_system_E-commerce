from atexit import register
from django.urls import path,include
from numpy import place
from . import views
from store.controller import authview,cart,wishlist,checkout,order


urlpatterns = [
    path('', views.home, name="home"),
    path('collections', views.collections, name="collections"),
    path('collections/<str:slug>', views.collectionsview, name="collectionsview"),
    path('collections/<str:cate_slug>/<str:prod_slug>', views.productview, name="productview"),
    
    path("product-list",views.productlistAjax),
    path('searchproduct',views.searchproduct, name="searchproduct"),


    path('register/',authview.register, name='register'),
    path('login/', authview.loginpage, name="loginpage"),
    path('logout/', authview.logoutpage, name="logout"),
    path('forget-password/', views.forget_password, name="forget_password"),
    path('forget-forget_password_first/', views.forget_password_first, name="forget_password_first"),

    path('add-to-cart', cart.addtocart, name="addtocart"),
    path('cart', cart.viewcart, name="cart"),
    path('update-cart', cart.updatecart, name="updatecart"),
    path('delete-cart-item', cart.deleteitem, name="deleteitem"),

    path('wishlist', wishlist.index, name="wishlist"),
    path('add-to-wishlist', wishlist.addtowishlist, name="addtowishlist"),
    path('delete-wishlist-item', wishlist.deletewishlistitem, name="deletewishlistitem"),
    
    path('checkout',checkout.index,name="checkout"),
    path('place-order', checkout.placeorder,name="placeorder"),
    path('my-orders', checkout.orders),

    path('my-orders', order.index,name="myorders"),
    path('view-order/<str:t_no>',order.vieworder,name="overview"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', authview.activate, name='activate'),
    path('captcha/', include('captcha.urls')),
]
