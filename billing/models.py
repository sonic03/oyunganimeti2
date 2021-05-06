from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
User = settings.AUTH_USER_MODEL

# Create your models here.

class BillingProfileManager(models.Manager):
    def new_or_get(self,request):
        user = request.user
        created=False
        obj=None
        if user.is_authenticated:
            obj,created=self.model.objects.get_or_create(user=user)
        return obj,created

class BillingProfile(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()


def user_create_receiver(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)

post_save.connect(user_create_receiver,sender=User)
