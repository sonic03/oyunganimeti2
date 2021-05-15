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

app_name='Management'

urlpatterns = [
    path('dashboard/',views.dashboard, name="dashboard"),
    path('site-users/',views.site_users, name="site_users"),
    path('repear-status/',views.rep_status,name="rep-status"),
    path('showcategory/',views.showcategory, name="showcategory"),
    path('login/',views.adminlogin,name='adminlogin'),
    path('logout/',views.adminlogout,name='adminlogout'),
    path('addcategory/',views.categoryadd,name='addcategory'),
    path('updatecategory/<str:id>',views.categoryupdate,name='updatecategory'),
    path('changestatus/<str:id>',views.change_status,name="change_status"),
    path('addproduct/',views.productadd,name='addproduct'),
    path('updateproduct/update/<int:id>',views.productupdate,name='updateproduct'),
    path('showproducts/',views.showproducts,name='showproducts'),
    path('subprice/<int:id>', views.subprice,name='subprice'),
    path('showsliders/',views.showsliders,name='showsliders'),
    path('addslider/',views.addslider,name='addslider'),
    path('delslider/<int:sliderid>',views.delslider,name='delslider'),
    path('addcommerce/',views.addcommerce,name='addcommerce'),
    path('showorders/',views.show_orders,name='showorders'),
    path('showorders/<str:order_id>',views.show_order_detail,name='showordersdetail'),
    path('showorders/update/<str:order_id>/<int:product_id>/<int:pincode_id>',views.update_order_detail,name='updateordersdetail'),
    path('showorders/add/<str:order_id>/<int:product_id>/',views.add_order_detail,name='addordersdetail'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

