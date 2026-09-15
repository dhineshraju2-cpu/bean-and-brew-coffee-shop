"""
URL configuration for coffee_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shop.views import home, register, profile, add_to_cart, cart, place_order, orders, order_detail, remove_from_cart, decrease_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('cart/add/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('place-order/', place_order, name='place_order'),
    path('orders/', orders, name='orders'),
    path('place-order/', place_order, name='place_order'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/decrease/<int:item_id>/', decrease_cart, name='decrease_cart'),
]
