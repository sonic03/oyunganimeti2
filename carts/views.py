import json
from django.core.mail import send_mail
from django.http.response import JsonResponse
from orders.models import Order
from django.db.models import query
from django.shortcuts import redirect, render
from .models import Cart
from products.models import Product
from datetime import datetime
from django.conf import settings
from billing.models import BillingProfile
from management.models import MyUser

User = settings.AUTH_USER_MODEL

def cart_create(user=None):
    cart_obj=Cart.objects.create(user=None)
    return cart_obj

def cart_home(request):
    #del request.session['card_id'] #session siler
    cart_obj,new_obj = Cart.objects.new_or_get(request)

    return render(request,'card.html',{'cart_obj':cart_obj})

def card_update(request,id):
    product_id =id
    product_obj = Product.objects.get(id=product_id)
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    cart_obj.products.add(product_obj)
    #print(request.session['card_id'])
    #return redirect('carts:cart_home')
    
    context={'cart_obj.products':list(cart_obj.products.all().values())}
    return JsonResponse(data=context)

def card_delete(request,id):
    product_id =id
    product_obj = Product.objects.get(id=product_id)
    cart_obj= Cart.objects.get(id=request.session['card_id'])
    cart_obj.products.remove(product_obj)
    #return redirect('carts:cart_home')
    context={'cart_obj.products':list(cart_obj.products.all().values())}
    return JsonResponse(data=context)

def checkout(request):
    cart_obj,cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0 :
        return redirect('carts:cart_home')


    billing_profile,billing_profile_created = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        order_obj,order_obj_created=Order.objects.new_or_get(billing_profile,cart_obj)
        
    if request.method=='POST':
        is_done=order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            del request.session['card_id']
            subject = 'Sipariş'
            message = """
                Merhaba Değerli Üyemi
                Oyunganimeti.com sitemizden {} tarihinde satın almış olduğunuz {} numaralı siparişinizi, siparişlerim sayfasından görüntüleyebilirsiniz.
                Banka hesabımıza ödemenizi yaptığınızda kodunuz teslim edilecektir.
                İyi oyunlar dileriz…

                Oyun Ganimeti Ailesi
            """.format(datetime.now().strftime("%D %H:%M:%S"),order_obj.order_id)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]
            send_mail( subject, message, email_from, recipient_list )
            #adminlere mail gönderimi:
            productlist=[]
            for p in order_obj.cart.products.all():
                productlist.append(p.name)
            subject = 'Siparişiniz Var!'
            message = """
                Yeni Sipariş Aldınız !

                Tarih: {}

                Sipariş Kodu: {}

                Ürünler: {}

                Oyun Ganimeti Ailesi
            """.format(datetime.now().strftime("%D %H:%M:%S"),order_obj.order_id,productlist)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = settings.RECIPIENT_LIST
            send_mail( subject, message, email_from, recipient_list )
            return redirect('carts:success')


    return render(request,'checkout.html',{'order_obj':order_obj,'billing_profile':billing_profile})
    
def check_out_done(request):
    
    return render(request,'succes.html')

def ccpayment(request):
    return render(request,"cc-payment.html")
