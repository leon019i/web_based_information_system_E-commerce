from atexit import register
from django.urls import path,include
from numpy import place
from . import views
from store.controller import authview,cart,wishlist,checkout,order
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name="home"),
    
    path('collections', views.collections, name="collections"),
    path('collections/<str:slug>', views.collectionsview, name="collectionsview"),
    path('collections/<str:cate_slug>/<str:prod_slug>', views.productview, name="productview"),
    path('collectionsearch/<str:slug>',views.collectionsearch,name='collectionsearch'),
    path('product-list',views.productlistAjax),
    path('searchproduct',views.searchproduct, name="searchproduct"),


    path('register/',authview.register, name='register'),
    path('login/', authview.loginpage, name="loginpage"),
    path('logout/', authview.logoutpage, name="logout"),
    path('passwordForm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', authview.passwordForm, name="passwordForm"),
    path('submit-password-form', authview.setpassword, name="changepassword"),
    path('forget-password/', views.forget_password, name="forget_password"),
    path('forget-forget_password_first/', views.forget_password_first, name="forget_password_first"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='store/registration/password_change_done.html'),name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='store/registration/password_change.html'), name='password_change'),

    path('add-to-cart', cart.addtocart, name="addtocart"),
    path('cart', cart.viewcart, name="cart"),
    path('update-cart', cart.updatecart, name="updatecart"),
    path('delete-cart-item', cart.deleteitem, name="deleteitem"),

    path('wishlist', wishlist.index, name="wishlist"),
    path('add-to-wishlist', wishlist.addtowishlist, name="addtowishlist"),
    path('delete-wishlist-item', wishlist.deletewishlistitem, name="deletewishlistitem"),
    path('profile',views.profile, name="profile"),
    path('profileForm', views.profileForm, name="profileForm"),
    
    path('checkout',checkout.index,name="checkout"),
    path('place-order', checkout.placeorder,name="placeorder"),
    path('my-orders', order.index,name="myorders"),
    
    path('view-order/<str:t_no>',order.vieworder,name="overview"),

    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', authview.activate, name='activate'),
    path('captcha/', include('captcha.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)