"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

app_name="Carts"

urlpatterns = [
    path('',views.cart_home, name="cart_home"),
    path('checkout/',views.checkout,name='checkout'),
    path('cc-payment/',views.ccpayment,name='cc-payment'),
    path('checkout/success',views.check_out_done,name='success'),
    path('update/<str:id>',views.card_update, name="cart_update"),
    path('delete/<str:id>',views.card_delete, name="cart_delete"),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

