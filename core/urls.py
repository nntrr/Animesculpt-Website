from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name="login"),  # Login page URL
    path('home/', views.home, name="home"),  # Home page URL

    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('store/', views.store, name="store"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('rewards/', views.rewardpage, name="rewards"),
    path('wheel/', views.wheelpage, name="wheel"),
    path('aboutus/', views.aboutuspage, name="aboutus"),
]
