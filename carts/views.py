import json
from django.core.mail import send_mail
from django.http.request import HttpHeaders, HttpRequest
from django.http.response import HttpResponseBase, HttpResponseGone, HttpResponseRedirect, JsonResponse
from django.middleware import csrf
from orders.models import Order
from django.db.models import query
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from .forms import KKForm
from .models import Cart
from products.models import Product
from datetime import datetime
from django.conf import settings
from billing.models import BillingProfile
from management.models import MyUser
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
import base64
import hmac
import hashlib
import requests
from decimal import *
from django.views.decorators.csrf import ensure_csrf_cookie

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
    user=request.user
    order=Order.objects.filter(Q(billing_profile_id=user.id) & Q(status='paid')).order_by('-timestamp').first()
    order_id=order.order_id
    print(order.order_total)
    


    return render(request,'succes.html',{'order_id':order_id})

@csrf_protect
def ccpayment(request):
    form=KKForm(request.POST or None)
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
    #guid="0c13d406-873b-403b-9c09-a5766840d98c" test için
    #cli_code="10738" test için
    #username="Test" test için
    #pwd="Test" test için
    guid="9F57F696-BD09-4B9F-8031-7476D02AED59"
    cli_code="37663"
    username="TP10068607"
    pwd="9F49402E0AB72B44"
    total = str(Decimal(order.order_total)).replace(".",",")
    siparis_ID = order.order_id
    ok_url = 'http://localhost:8000/profile/orders/'
    fail_url = 'http://localhost:8000/'
    
    if request.method=="POST":
        if form.is_valid:
            isim=request.POST.get("isim")
            kkno=request.POST.get("kkno")
            skay=request.POST.get("skay")
            skyil=request.POST.get("skyil")
            cvc=request.POST.get("cvc")
            gsm=request.POST.get("gsm")
            
            print(isim)
            print(kkno)
            print(skay)
            print(skyil)
            print(cvc)
            print(gsm)
            print(total)

            print(siparis_ID)
            hash_token=cli_code+guid+total+total+siparis_ID+fail_url+ok_url
            print(hash_token)
            adress="https://posws.param.com.tr/turkpos.ws/service_turkpos_prod.asmx?WSDL"
            headers = {
                'Content-type':'text/xml', 
                'Accept':'text/xml'
            }

            body="""<?xml version="1.0" encoding="utf-8"?> <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"> <soap:Body>
            <SHA2B64 xmlns="https://turkpos.com.tr/">
            <Data>"""+hash_token+"""</Data>
            </SHA2B64>
            </soap:Body>
            </soap:Envelope>"""

            response=requests.post(adress,headers=headers,data=body)

            token=response.text[response.text.index("<SHA2B64Result>")+len("</SHA2B64Result>")-1:response.text.index("</SHA2B64Result>")]
            print("token: " + token)
            adress2="https://posws.param.com.tr/turkpos.ws/service_turkpos_prod.asmx?WSDL"
            body2="""<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <TP_Islem_Odeme_OnProv_WMD xmlns="https://turkpos.com.tr/">
                <G>
                    <CLIENT_CODE>{}</CLIENT_CODE>
                    <CLIENT_USERNAME>{}</CLIENT_USERNAME>
                    <CLIENT_PASSWORD>{}</CLIENT_PASSWORD>
                </G>
                <GUID>{}</GUID>
                <KK_Sahibi>{}</KK_Sahibi>
                <KK_No>{}</KK_No>
                <KK_SK_Ay>{}</KK_SK_Ay>
                <KK_SK_Yil>{}</KK_SK_Yil>
                <KK_CVC>{}</KK_CVC>
                <KK_Sahibi_GSM>{}</KK_Sahibi_GSM>
                <Hata_URL>{}</Hata_URL>
                <Basarili_URL>{}</Basarili_URL>
                <Siparis_ID>{}</Siparis_ID>
                <Siparis_Aciklama>string</Siparis_Aciklama>
                <Islem_Tutar>{}</Islem_Tutar>
                <Toplam_Tutar>{}</Toplam_Tutar>
                <Islem_Hash>{}</Islem_Hash>
                <Islem_Guvenlik_Tip>NS</Islem_Guvenlik_Tip>
                <Islem_ID>{}</Islem_ID>
                <IPAdr>{}</IPAdr>
                <Ref_URL>https://dev.param.com.tr/tr</Ref_URL>
                <Data1>string</Data1>
                <Data2>string</Data2>
                <Data3>string</Data3>
                <Data4>string</Data4>
                <Data5>string</Data5>
                
                </TP_Islem_Odeme_OnProv_WMD>
            </soap:Body>
            </soap:Envelope>""".format(cli_code,username,
                                        pwd,guid,isim,
                                        kkno,skay,skyil,
                                        cvc,gsm,fail_url,ok_url,siparis_ID,
                                        total,total,token,siparis_ID,ip)
            
            response2=requests.post(adress2,headers=headers,data=body2.encode('utf-8'))
            print(response2.text)
            result=response2.text[response2.text.index("<Sonuc>")+len("<Sonuc>"):response2.text.index("</Sonuc>")]
            if int(result) == -207:
                return HttpResponse('<h1>Sistem Hatası</h1>')
            #result3d=response2.text[response2.text.index("<UCD_HTML>")+len("<UCD_HTML>"):response2.text.index("</UCD_HTML>")]
            #result3d=result3d.replace("&lt;","<")
            #result3d=result3d.replace("&gt;",">")
            #result3d=result3d.replace('<input type="hidden" name="_charset_" value="UTF-8"/>','<input type="hidden" name="csrfmiddlewaretoken" value="'+request.META["CSRF_COOKIE"]+'"><input type="hidden" name="_charset_" value="UTF-8"/>')
            
            
            #print(result3d)
            
            print(result)
            
            print(request.META["CSRF_COOKIE"])
            
            if int(result) > 0:
                #return HttpResponse(result3d,content_type="text/html")
                order=Order.objects.filter(Q(order_id=order.order_id)).first()
                order.status='Kart Ödemesi'
                order.save()
                return render(request,"cart-success.html")
            else:
                return render(request,"cart-fail.html")

   





    return render(request,"cc-payment.html",{'form':form,'total':order.order_total})



@csrf_exempt
def callback(request):

    if request.method != 'POST':
        return HttpResponse(str(''))
    else:

        post = request.POST

        # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        merchant_key = b'6NnX3CCQjo73Mdk4'
        merchant_salt = 'zasJCnqC6ZfgwXra'

        # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        # POST değerleri ile hash oluştur.
        hash_str = str(post['merchant_oid']) + str(merchant_salt) + str(post['status']) + str(post['total_amount'])
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
        

        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        #if hash != post['hash']:
        #    return HttpResponse(str('PAYTR notification failed: bad hash'))

        # BURADA YAPILMASI GEREKENLER
        # 1) Siparişin durumunu post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
        # 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse "OK" yaparak sonlandırın.
        order_status=Order.objects.filter(order_id=str(post['merchant_oid'])).first().status
        if order_status == 'paid':
            return HttpResponse(str('OK'))
        
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

