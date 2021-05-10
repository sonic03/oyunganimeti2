from django.db import models
from django.conf import settings
from django.db.models.fields import related
from django.db.models.signals import pre_save, post_save ,m2m_changed

from products.models import Product,PinCode
# Create your models here.
MyUser = settings.AUTH_USER_MODEL



class CartManager(models.Manager):
    def new_or_get(self, request):
        card_id=request.session.get('card_id',None)
        qs=self.get_queryset().filter(id=card_id)
        if qs.count() == 1:
            new_obj=False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None: #siteye giriş yapmadan ürün ekleyip siteye girince sepetten devam etmesi için
                cart_obj.user = request.user
                cart_obj.save()

        else:
            cart_obj = Cart.objects.new(user=None)
            new_obj=True
            request.session['card_id']=cart_obj.id
        return cart_obj, new_obj

    def new(self,user=None):
        user_obj=None
        if user is not None:
            if user.is_authenticated():
                user_obj=user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user=models.ForeignKey(MyUser,null=True,blank=True,on_delete=models.SET_NULL)
    products = models.ManyToManyField(Product,blank=True)
    subtotal = models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    total = models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    pin_code = models.ManyToManyField(PinCode,blank=True)

    objects = CartManager()



def m2m_change_cart_receiver(sender, instance, action,*args, **kwargs):
    if action=="post_add" or action=="post_remove" or action == "post_clear":
        products = instance.products.all()
        total = 0
        for product in products:
            total += product.discount_price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_change_cart_receiver,sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance,*args, **kwargs):
    instance.total = instance.subtotal # * kdv oranı

pre_save.connect(pre_save_cart_receiver,sender=Cart)