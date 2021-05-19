from itertools import zip_longest
from django import forms
from django.contrib.sites import requests
from management.models import MyUser
from django.shortcuts import render, get_object_or_404,redirect
from .models import  Category,Product,Slider,Commerce
from carts.models import Cart
from .forms import LoginSiteForm,RegisterSiteForm,ContantForm
from django.contrib.auth import authenticate, login, get_user_model,logout
import json
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
from django.conf import settings
from billing.models import BillingProfile
from orders.models import Order
from management.decorators import bakim
from django.db.models import Q
# Create your views here.

User = settings.AUTH_USER_MODEL

@bakim
def index(request):
    if settings.REPAIR_MODE:
        return render(request,'bakim.html')
    else:
        sliders=[]
        products=Product.objects.all()
        slider=Slider.objects.all()
        for s in slider:sliders.append(s.slider.url)
        
        cc=json.dumps(sliders)
        
        
        
        
        commerce = Commerce.objects.all()
        discount_product = Product.objects.filter(Q(discounted=True) & Q(active=True)).order_by('-id')[0:5]
        new_product = Product.objects.filter(Q(news=True) & Q(active=True)).order_by('-id')[0:5]
        most_seller = Product.objects.filter(Q(most_seller=True) & Q(active=True)).order_by('-id')[0:5]
        return render(request,'index.html',{'products':products,'slider':slider,'commerce':commerce,'discount_product':discount_product,'cc':cc,'new_product':new_product,'most_seller':most_seller})


def navbar(request):
    
    category=Category.objects.filter(active=True)
    cart_id = request.session.get('card_id')
    if cart_id is not None:
        cart_count = Cart.objects.get(id=cart_id)
    else:
        cart_count = None
    return {'category':category,'cart_count':cart_count}

@bakim
def hakkimizda(request):
    
    return render(request,"hakkimizda.html")

@bakim
def kvkk(request):
   
    return render(request,"kvkk.html")

@bakim
def ks(request):
    
    return render(request,"kullanici-sozlesmesi.html")

@bakim
def category(request,slug):
    
    ct=get_object_or_404(Category,slug=slug)
    product=Product.objects.filter(Q(category=ct) & Q(active=True))
    return render(request,'category.html',{'product':product,'ct':ct})

@bakim
def loginsite(request):
    form = LoginSiteForm(request.POST or None)
    context = {"form": form, 'recaptcha_site_key': settings.GOOGLE_RECAPTCHA_SITE_KEY}
    if form.is_valid():
        #recaptcha_response = request.POST.get('g-recaptcha-response')
        #data = {
        #    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        #    'response': recaptcha_response
        #}
        #r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        #result = r.json()
        #if result['success']:
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if not user.admin:
                login(request, user)
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                subject = 'Siteye Giriş'
                message = """
                    Merhaba Değerli Üyemiz
    
                    {} tarihinde, {} ip adresinden sitemize giriş yapılmıştır. Bu kişi siz değilseniz en kısa sürede irtibata geçiniz.
    
                    Oyun Ganimeti Ailesi
                """.format(datetime.now().strftime("%D %H:%M:%S"),ip)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail( subject, message, email_from, recipient_list )
                return redirect('index')
    else:
        messages.error(request, 'reCAPTCHA hatalı. Lütfen tekrar deneyin')


    return render(request, "sitelogin.html", context)

@bakim
def registersite(request):
    form = RegisterSiteForm(request.POST or None)
    if form.is_valid():
        #recaptcha_response = request.POST.get('g-recaptcha-response')
        #data = {
        #    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        #    'response': recaptcha_response
        #}
        #r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        #result = r.json()
        #if result['success']:
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        user = MyUser(email=email)
        user.set_password(password)
        user.save()
        login(request, user)
        subject = 'Kayıt Formu'
        message = """
            Merhaba Değerli Üyemi
            Sitemize Üye olduğunuz için teşekkür ederiz.
            {} tarihinde, {} ip adresinden sitemize tarafınızdan kayıt yapılmıştır.
            Oyun Ganimeti Ailesi
        """.format(datetime.now().strftime("%D %H:%M:%S"),ip)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail( subject, message, email_from, recipient_list )
        return redirect('index')

    else:
        messages.error(request, 'reCAPTCHA hatalı. Lütfen tekrar deneyin')
        
            

    return render(request, "siteregister.html", {'form': form})

@bakim
def sitelogout(request):
    logout(request)
    return redirect('index')

@bakim
def user_order_page(request):
    user_id=request.user.id
    billing_profile_id=BillingProfile.objects.filter(user_id=user_id)[0].id
    orders=Order.objects.filter(billing_profile_id=billing_profile_id).exclude(status='created').order_by("-timestamp")

    return render(request,'orders.html',{'orders':orders})

@bakim
def user_order_page_detail(request,order_id):
    
    order_detail=Order.objects.filter(order_id=order_id).prefetch_related('cart').first()
    
    if order_detail.billing_profile.user_id==request.user.id:
        order_list=list(zip_longest(order_detail.cart.products.all(),order_detail.cart.pin_code.all(),fillvalue='tedaik aşamasında'))
        return render(request,'orderdetail.html',{'order_detail':order_detail,'order_list':order_list})
    else:
        return redirect('index')

@bakim
def pros(request):
    pros= Product.objects.all()
    return render(request, "products.html", {"pros": pros})

@bakim
def sss(request):
   
    return render(request, "sss.html")




def bakim(request):
    return render(request,"bakim.html")


def contact(request):
    form = ContantForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        msg = form.cleaned_data.get('msg')
        subject = 'iletişim Formu'
        message = """
            İletişim mesajı Aldınız !

            İsim Soyisim: {}
            
            Email: {}
            
            Telefon: {}
            
            Mesaj {}    
            
            Oyun Ganimeti Ailesi
        """.format(name,email,phone,msg)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = settings.RECIPIENT_LIST
        send_mail( subject, message, email_from, recipient_list )
        return redirect('index')
    else:
        messages.error(request, 'reCAPTCHA hatalı. Lütfen tekrar deneyin')


    return render(request, "iletisim.html", context)



def mesafelisatissozlesmesi(request):
   
    return render(request, "satis-sozlesmesi.html")


def gizlilik(request):
   
    return render(request, "gizlilik.html")


def iade(request):
   
    return render(request, "iade.html")