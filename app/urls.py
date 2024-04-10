from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    # Các URL patterns khác của ứng dụng của bạn
    path('register/',views.register, name="register"),
    path('login/',views.loginPage, name="login"),
    path('search/',views.search, name="search"),
    path('category/',views.category, name="category"),
    path('detail/',views.detail, name="detail"),
    path('logout/',views.logoutPage, name="logout"),
    path('cart/',views.cart, name="cart"),
    path('payment/',views.payment, name="payment"),
    path('checkout/',views.checkout, name="checkout"),
    path('update_item/',views.updateItem, name="update_item"),
    path('about/',views.about, name="about"),
   
]

