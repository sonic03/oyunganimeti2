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
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import hmac
import hashlib
import requests


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
            #subject = 'Sipariş'
            #message = """
            #    Merhaba Değerli Üyemi
            #    Oyunganimeti.com sitemizden {} tarihinde satın almış olduğunuz {} numaralı siparişinizi, siparişlerim sayfasından görüntüleyebilirsiniz.
            #    Banka hesabımıza ödemenizi yaptığınızda kodunuz teslim edilecektir.
            #    İyi oyunlar dileriz…
#
            #    Oyun Ganimeti Ailesi
            #""".format(datetime.now().strftime("%D %H:%M:%S"),order_obj.order_id)
            #email_from = settings.EMAIL_HOST_USER
            #recipient_list = [request.user.email]
            #send_mail( subject, message, email_from, recipient_list )
            ##adminlere mail gönderimi:
            #productlist=[]
            #for p in order_obj.cart.products.all():
            #    productlist.append(p.name)
            #subject = 'Siparişiniz Var!'
            #message = """
            #    Yeni Sipariş Aldınız !
#
            #    Tarih: {}
#
            #    Sipariş Kodu: {}
#
            #    Ürünler: {}
#
            #    Oyun Ganimeti Ailesi
            #""".format(datetime.now().strftime("%D %H:%M:%S"),order_obj.order_id,productlist)
            #email_from = settings.EMAIL_HOST_USER
            #recipient_list = settings.RECIPIENT_LIST
            #send_mail( subject, message, email_from, recipient_list )
            return redirect('carts:success')


    return render(request,'checkout.html',{'order_obj':order_obj,'billing_profile':billing_profile})
    
def check_out_done(request):
    user=request.user
    order=Order.objects.filter(Q(billing_profile_id=user.id) & Q(status='paid')).order_by('-timestamp').first()
    order_id=order.order_id
    print(order.order_total)
    


    return render(request,'succes.html',{'order_id':order_id})

def ccpayment(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    order=Order.objects.filter(Q(billing_profile_id=request.user.id) & Q(status='paid')).order_by('-timestamp').first()
    all_pros=[]
    cart_id=order.cart_id
    products=Cart.objects.filter(id=cart_id).prefetch_related('products').first().products.all()
    for p in products:
        list_p=[str(p.name),str(p.discount_price),1]
        all_pros.append(list_p)
    merchant_id = '238265'
    merchant_key = b'eNPyHwKtT7CNZwb2'
    merchant_salt = b'zasJCnqC6ZfgwXra'
    email = request.user.email
    payment_amount = str(int(order.order_total*100))
    merchant_oid = order.order_id
    user_name = request.user.email
    user_address = 'deneme1'
    user_phone = request.user.phone
    merchant_ok_url = 'https://www.oyunganimeti.com/profile/orders/'
    merchant_fail_url = 'https://www.oyunganimeti.com/'
    user_basket=base64.b64encode(json.dumps(all_pros).encode())
    user_ip = ip
    debug_on = '1'
    timeout_limit = '30'
    # Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
    test_mode = '1'

    no_installment = '0' # Taksit yapılmasını istemiyorsanız, sadece tek çekim sunacaksanız 1 yapın

    # Sayfada görüntülenecek taksit adedini sınırlamak istiyorsanız uygun şekilde değiştirin.
    # Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur.
    max_installment = '0'

    currency = 'TL'

    hash_str = merchant_id + user_ip + merchant_oid + email + payment_amount + user_basket.decode() + no_installment + max_installment + currency + test_mode
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())
    params = {
    'merchant_id': merchant_id,
    'user_ip': user_ip,
    'merchant_oid': merchant_oid,
    'email': email,
    'payment_amount': payment_amount,
    'paytr_token': paytr_token,
    'user_basket': user_basket,
    'debug_on': debug_on,
    'no_installment': no_installment,
    'max_installment': max_installment,
    'user_name': user_name,
    'user_address': user_address,
    'user_phone': user_phone,
    'merchant_ok_url': merchant_ok_url,
    'merchant_fail_url': merchant_fail_url,
    'timeout_limit': timeout_limit,
    'currency': currency,
    'test_mode': test_mode
    }
    result = requests.post('https://www.paytr.com/odeme/api/get-token', params)
    res = json.loads(result.text)
    if res['status'] == 'success':
        print(res['token'])

        
        context = {
            'token': res['token']
        }
        
    else:
        print(result.text)





    return render(request,"cc-payment.html",context)



@csrf_exempt
def callback(request):

    if request.method != 'POST':
        return HttpResponse(str(''))

    post = request.POST

    # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_key = b'eNPyHwKtT7CNZwb2'
    merchant_salt = 'zasJCnqC6ZfgwXra'

    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    # POST değerleri ile hash oluştur.
    hash_str = post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
    hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())

    # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
    # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
    # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    if hash != post['hash']:
        return HttpResponse(str('PAYTR notification failed: bad hash'))

    # BURADA YAPILMASI GEREKENLER
    # 1) Siparişin durumunu post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
    # 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse "OK" yaparak sonlandırın.
    print(post['merchant_oid'])
    print('*********')

    if post['status'] == 'success':  # Ödeme Onaylandı
        """
        BURADA YAPILMASI GEREKENLER
        1) Siparişi onaylayın.
        2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
        3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda değişebilir. 
        Güncel tutarı post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
        """
        print(request)
    else:  # Ödemeye Onay Verilmedi
        """
        BURADA YAPILMASI GEREKENLER
        1) Siparişi iptal edin.
        2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
        post['failed_reason_code'] - başarısız hata kodu
        post['failed_reason_msg'] - başarısız hata mesajı
        """
        print(request)

    # Bildirimin alındığını PayTR sistemine bildir.
    return HttpResponse(str('OK'))

def paytr(request):

    return render(request,'paytr.html')

