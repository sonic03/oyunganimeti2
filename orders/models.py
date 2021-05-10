from django.db import models
from django.db.models.signals import pre_save, post_save ,m2m_changed
from carts. models import Cart
import random
import string
from .utils import id_generator, unique_id
# Create your models here.
from billing.models import BillingProfile

ORDER_STATUS=(
    ('created','Oluşturuldu'),
    ('paid','Tedarik Aşamasında'), #ödemesi yapılmış ise 
    ('deliver','Teslim Edildi'),
    ('cancel','İptal Edildi'),
)


class OrderManager(models.Manager):
    def new_or_get(self,billing_profile,cart_obj):
        qs = self.get_queryset().filter(billing_profile=billing_profile,cart=cart_obj, active=True,status='created').exclude(status='paid')
        if qs.count==1:
            obj=qs.first()
            created=False
        else:
            obj= self.model.objects.create(billing_profile=billing_profile,cart=cart_obj)
            created=True
        return obj,created


class Order(models.Model):
    order_id=models.CharField(max_length=120,blank=True)
    billing_profile=models.ForeignKey(BillingProfile,null=True,blank=True,on_delete=models.SET_NULL)
    cart = models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True)
    status= models.CharField(max_length=120,default='created',choices=ORDER_STATUS)
    order_total = models.DecimalField(default="0.00",max_digits=100,decimal_places=2)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    objects=OrderManager()

    
    def update_total(self):
        self.order_total=self.cart.total
        self.save()
        return self.order_total

    def check_done(self):
        billing_profile=self.billing_profile
        total = self.order_total
        if billing_profile and total > 0:
            return True
        return False
    
    def mark_paid(self):
        if self.check_done():
            self.status='paid'
            self.save()
        return self.status



def post_save_cart_total(sender,instance,created,*args, **kwargs):
    if not created:
        cart_obj=instance
        cart_total=cart_obj.total
        cart_id=cart_obj.id
        qs=Order.objects.filter(cart__id=cart_id)
        if qs==1:
            order_obj=qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total,sender=Cart)

def post_save_order(sender,instance,created,*args, **kwargs):
    if created:
        instance.update_total()
       

post_save.connect(post_save_order,sender=Order)

def pre_save_create_order_id(sender,instance,*args, **kwargs):
    if not instance.order_id:
        instance.order_id=unique_id(instance)

pre_save.connect(pre_save_create_order_id,sender=Order)


def pre_save_order_instance(sender,instance,*args, **kwargs):
    older_qs=Order.objects.exclude(billing_profile=instance.billing_profile).filter(cart=instance.cart)
    if older_qs.exists():
        older_qs.update(active=False)
pre_save.connect(pre_save_order_instance,sender=Order)