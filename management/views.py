from datetime import datetime
from core.models import Repeary
from management.decorators import is_login_and_admin,not_authenticate
from carts.models import Cart
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, get_user_model,logout
from django.shortcuts import render, redirect, get_object_or_404
from itertools import zip_longest


from .forms import LoginForm,PinDeliveryForm


# Create your views here.
from products.forms import CategoryAddForm,ProductAddForm,SliderForm,CommerceForm
from products.models import Category,Product,Slider,Commerce,PinCode
from orders.models import Order

@is_login_and_admin
def dashboard(request):
    return render(request, 'dashboard.html')

@is_login_and_admin
def showcategory(request):
    category = Category.objects.all()
    return render(request, "showcategory.html", {'category': category})


User = get_user_model()

@not_authenticate
def adminlogin(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        print(email)
        print(password)
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            if user.admin:
                login(request, user)
                return redirect('management:dashboard')
            else:
                return redirect('index')

    return render(request, "adminlogin.html", {'form': form})

@is_login_and_admin
def adminlogout(request):
    logout(request)
    return redirect('index')

@is_login_and_admin
def categoryadd(request):
    form = CategoryAddForm(request.POST or None,request.FILES or None)
    if request.method =='POST':
        if form.is_valid():
            form.save()
            return redirect('management:showcategory')
    return render(request, 'addcategory.html', {'form': form})

@is_login_and_admin
def categoryupdate(request,id):
    category=get_object_or_404(Category,id=id)
    form = CategoryAddForm(request.POST or None,request.FILES or None,instance=category)
    if request.method =='POST':
        if form.is_valid():
            form.save()
            return redirect('management:showcategory')
    return render(request, 'addcategory.html', {'form': form})


@is_login_and_admin
def change_status(request,id):
    cat=Category.objects.filter(id=id).first()
    if cat.active:
        cat.active=False
    else:
        cat.active=True
    cat.save()
    return redirect('management:showcategory')

@is_login_and_admin
def productadd(request):
    form = ProductAddForm(request.POST or None,request.FILES or None)
    if request.method =='POST':
        if form.is_valid():
            form.save()
            return redirect('management:showproducts')
    return render(request, 'addproduct.html', {'form': form})

@is_login_and_admin
def productupdate(request,id):
    product=get_object_or_404(Product,id=id)
    form = ProductAddForm(request.POST or None,request.FILES or None,instance=product)
    if request.method =='POST':
        if form.is_valid():
            form.save()
            return redirect('management:showproducts')
    return render(request, 'updateproduct.html', {'form': form})


@is_login_and_admin
def showproducts(request):
    products = Product.objects.all()
    return render(request, "showproducts.html", {'products': products})

@is_login_and_admin
def subprice(request,id):
    product=get_object_or_404(Product,id=id)
    if not product.main:
        products=Product.objects.filter(main_id=product.id)
        for p in products:
            p.discount_price=product.discount_price
            p.save()
        return redirect('management:showproducts')

@is_login_and_admin
def showsliders(request):
    sliders=Slider.objects.all()
    commerce = Commerce.objects.all()

    return render(request,'showsliders.html',{'sliders':sliders,'commerce':commerce})
@is_login_and_admin
def addslider(request):
    form=SliderForm(request.POST or None,request.FILES or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('management:showsliders')
    return render(request,'slideradd.html',{'form':form})

@is_login_and_admin
def delslider(request,sliderid):
    slider=get_object_or_404(Slider,id=sliderid)
    slider.delete()
    return redirect('management:showsliders')
    

@is_login_and_admin   
def addcommerce(request):
    form=CommerceForm(request.POST or None,request.FILES or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('management:showsliders')
    return render(request,'commerceadd.html',{'form':form})



@is_login_and_admin
def site_users(request):
    users=User.objects.all()

    return render(request,'site-user.html',{'users':users})

@is_login_and_admin
def show_orders(request):
    orders=Order.objects.all().order_by("-timestamp")

    return render(request,'showorders.html',{'orders':orders})

@is_login_and_admin
def show_order_detail(request,order_id):
    
    order_detail=Order.objects.filter(order_id=order_id).prefetch_related('cart').first()

    order_list=list(zip_longest(order_detail.cart.products.all(),order_detail.cart.pin_code.all(),fillvalue='tedaik aşamasında'))
    oldorderid=order_detail.id
    if len(order_detail.cart.products.all())==len(order_detail.cart.pin_code.all()):
        
        order_detail.status='Teslim Edildi' 
        order_detail.save()  
        subject = 'Sipariş'
        message = """
            Merhaba Değerli Üyemiz
           {} numaralı siparişiniz teslim edilmiştir.
            
            İyi oyunlar dileriz…
            Oyun Ganimeti Ailesi
        """.format(order_id)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [order_detail.billing_profile.user.email]
        send_mail( subject, message, email_from, recipient_list )   
    

    return render(request,'showorderdetails.html',{'order_detail':order_detail,'order_list':order_list})


@is_login_and_admin
def add_order_detail(request,order_id,product_id):
    order_detail=Order.objects.filter(order_id=order_id).prefetch_related('cart').first()
    
    cart_id=order_detail.cart_id
    ss=Cart.objects.filter(id=cart_id).prefetch_related('pin_code').prefetch_related('products').first()
    form=PinDeliveryForm(request.POST or None) 
    if form.is_valid():
        epin=form.cleaned_data.get('pin_code')
        
        newEpin=Cart.objects.filter(id=cart_id,products__id=product_id).prefetch_related('pin_code').first()
        
        pinobj=PinCode(pin_code=epin,product_id=product_id)
        
        pinobj.save()
        
        newEpin.pin_code.add(pinobj)
        newEpin.cart_id=cart_id
        newEpin.save()
        return redirect("management:showordersdetail" ,order_id=order_id)
    

    
    return render(request,'addorderdetail.html',{'form':form})

@is_login_and_admin
def update_order_detail(request,order_id,product_id,pincode_id):
    order_detail=Order.objects.filter(order_id=order_id).prefetch_related('cart').first()
    
    cart_id=order_detail.cart_id
    #ss=Cart.objects.filter(id=cart_id).prefetch_related('pin_code').prefetch_related('products').first().pin_code.get(id=pincode_id).pin_code
    pin=get_object_or_404(PinCode,id=pincode_id)

    print(pin)
    form=PinDeliveryForm(request.POST or None,instance=pin) 
    if form.is_valid():
        epin=form.cleaned_data.get('pin_code')
        print("1.adım çalıştı")
        newEpin=Cart.objects.filter(id=cart_id,products__id=product_id).prefetch_related('pin_code').first()
        print("2.adım çalıştı")
        print(epin)
        print(type(epin))
        pinobj=PinCode(id=pincode_id,pin_code=epin,product_id=product_id)
        print(pinobj)
        pinobj.save()
        print(pinobj)
        newEpin.pin_code.add(pinobj)
        
        print("3.adım çalıştı")
        #newEpin.pin_code.save()
        print("4.adım çalıştı")
        newEpin.cart_id=cart_id
        newEpin.save()
       
        print(epin)
        
        return redirect("management:showordersdetail" ,order_id=order_id)
        
    

    
    return render(request,'epinupdate.html',{'form':form})


def change_rep_status(request):
    rep=settings.REPAIR_MODE
    
    return {'rep':rep}

def rep_status(request):
    
    if settings.REPAIR_MODE:
        settings.REPAIR_MODE=False
    else:
        settings.REPAIR_MODE=True
    return redirect("management:dashboard")