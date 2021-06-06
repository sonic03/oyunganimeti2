from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,password=None,is_active=True,is_staff=False,is_admin=False,is_site_user=True,is_author=False):
        if not email:
            raise ValueError("Kullanıcının epostası olmalıdır")
        if not password:
            raise ValueError("Kullanıcının parolası olmalıdır")

        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.active=is_active 
        user_obj.author=is_author
        user_obj.site_user=is_site_user
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,email,password=None):
        user=self.create_user(email,password=password,is_staff=True)
        return user
    def create_superuser(self,email,password=None):
        user = self.create_user(email, password=password, is_staff=True,is_admin=True)
        return user



class MyUser(AbstractBaseUser):

    email = models.EmailField(max_length=255, verbose_name='Email', unique=True)
    phone = models.CharField(max_length=11,verbose_name="Telefon Numarası",default='05555555555')
    active = models.BooleanField(default=True, verbose_name='Aktif')  # siteye girebilir
    staff = models.BooleanField(default=False, verbose_name='Site Elemanı')
    admin = models.BooleanField(default=False, verbose_name='Admin')
    site_user = models.BooleanField(default=True, verbose_name='Site Üyesi')
    author = models.BooleanField(default=False, verbose_name='Yazar')



    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_site_user(self):
        return self.admin

    @property
    def is_author(self):
        return self.admin    


class Profile(models.Model):
    user = models.OneToOneField(MyUser,null=True,on_delete=models.SET_NULL)



