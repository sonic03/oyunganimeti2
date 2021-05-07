from itertools import zip_longest
from django import forms
from management.models import MyUser
from django.shortcuts import render, get_object_or_404,redirect
from .models import  Category,Product,Slider,Commerce,DiscountProduct,NewProduct
from carts.models import Cart
from .forms import LoginSiteForm,RegisterSiteForm
from django.contrib.auth import authenticate, login, get_user_model,logout
import json
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
from django.conf import settings
from billing.models import BillingProfile
from orders.models import Order
# Create your views here.

User = settings.AUTH_USER_MODEL

def index(request):
    sliders=[]
    products=Product.objects.all()
    slider=Slider.objects.all()
    for s in slider:sliders.append(s.slider.url)
    
    cc=json.dumps(sliders)
    
    
    
    pr4=Product.objects.all()[0:4]
    commerce = Commerce.objects.all()
    discount_product = DiscountProduct.objects.order_by('-id')[0:4]
    new_product = NewProduct.objects.order_by('-id')[0:4]
    return render(request,'index.html',{'products':products,'slider':slider,'pr4':pr4,'commerce':commerce,'discount_product':discount_product,'cc':cc,'new_product':new_product})

def navbar(request):
    category=Category.objects.filter(active=True)
    cart_id = request.session.get('card_id')
    if cart_id is not None:
        cart_count = Cart.objects.get(id=cart_id)
    else:
        cart_count = None
    return {'category':category,'cart_count':cart_count}

def hakkimizda(request):
    return render(request,"hakkimizda.html")

def kvkk(request):
    return render(request,"kvkk.html")

def ks(request):
    return render(request,"kullanici-sozlesmesi.html")

def category(request,slug):
    ct=get_object_or_404(Category,slug=slug)
    product=Product.objects.filter(category=ct)
    return render(request,'category.html',{'product':product,'ct':ct})

def loginsite(request):
    form = LoginSiteForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        
        user = authenticate(request, username=email, password=password)
      
        if user is not None:
                login(request, user)
                #subject = 'Siteye Giriş'
                #message = """
                #    Merhaba Değerli Üyemiz
#
                #    {} tarihinde, {} ip adresinden sitemize giriş yapılmıştır. Bu kişi siz değilseniz en kısa sürede irtibata geçiniz.
#
                #    Oyun Ganimeti Ailesi
                #""".format(datetime.now().strftime("%D %H:%M:%S"),request.META['REMOTE_ADDR'])
                #email_from = settings.EMAIL_HOST_USER
                #recipient_list = [user.email]
                #send_mail( subject, message, email_from, recipient_list )
                return redirect('index')
            

    return render(request, "sitelogin.html", {'form': form})

def registersite(request):
    form = RegisterSiteForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        
        
        user = MyUser(email=email)
        user.set_password(password)
        user.save()
        login(request, user)       
        #subject = 'Kayıt Formu'
        #message = """
        #    Merhaba Değerli Üyemi
        #    Sitemize Üye olduğunuz için teşekkür ederiz.
        #    {} tarihinde, {} ip adresinden sitemize tarafınızdan kayıt yapılmıştır.
        #    Oyun Ganimeti Ailesi
        #""".format(datetime.now().strftime("%D %H:%M:%S"),request.META['REMOTE_ADDR'])
        #email_from = settings.EMAIL_HOST_USER
        #recipient_list = [user.email]
        #send_mail( subject, message, email_from, recipient_list )
        return redirect('index')
    else:
        print(form.errors)
        
            

    return render(request, "siteregister.html", {'form': form})

def sitelogout(request):
    logout(request)
    return redirect('index')

def user_order_page(request):
    user_id=request.user.id
    billing_profile_id=BillingProfile.objects.filter(user_id=user_id)[0].id
    orders=Order.objects.filter(billing_profile_id=billing_profile_id).exclude(status='created').order_by("-timestamp")

    return render(request,'orders.html',{'orders':orders})

def user_order_page_detail(request,order_id):
    
    order_detail=Order.objects.filter(order_id=order_id).prefetch_related('cart').first()
    
    if order_detail.billing_profile.user_id==request.user.id:
        order_list=list(zip_longest(order_detail.cart.products.all(),order_detail.cart.pin_code.all(),fillvalue='tedaik aşamasında'))
        return render(request,'orderdetail.html',{'order_detail':order_detail,'order_list':order_list})
    else:
        return redirect('index')


def pros(request):
    pros=Product.objects.all()
    return render(request,"products.html",{"pros":pros})