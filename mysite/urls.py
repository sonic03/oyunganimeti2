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
from django.urls import path, include
from django.views.generic import TemplateView
from products import views
from carts.views import callback

urlpatterns = [
                  path('login/', views.loginsite, name="loginsite"),
                  path('logout/', views.sitelogout, name="logout"),
                  path('register/', views.registersite, name="registersite"),
                  path('card/', include("carts.urls", namespace='carts')),
                  path('', views.index, name='index'),
                  path('<slug:slug>/', views.category, name='category'),
                  path('management/', include('management.urls', namespace="management")),
                  path('profile/orders/', views.user_order_page, name="user_orders"),
                  path('profile/orders/<str:order_id>/', views.user_order_page_detail, name="user_orders_detail"),
                  path('kullanici-sozlesmesi', views.ks,
                       name="kullanici-sozlesmesi"),
                  path('hakkimizda', views.hakkimizda, name="hakkimizda"),
                  path('kvkk', views.kvkk, name="kvkk"),
                  path('products',views.pros,name="pros"),
                  path('bakim',views.bakim,name="bakim"),
                  path('sss', views.sss, name="sss"),
                  path('contact', views.contact, name="contact"),
                  path('mesafeli-satis-sozlesmesi',views.mesafelisatissozlesmesi,name="mesafelisatissozlesmesi"),
                  path('gizlilik-politikasi',views.gizlilik,name="gizlilik"),
                  path('iade',views.iade,name="iade"),
                  path('paytr/result',callback,name="callback"),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
