from django.db import models
from django.db.models.base import Model


# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name='Kategori Adı', max_length=200)
    desc = models.TextField(verbose_name='Aaçıklama', max_length=200)
    cat_img = models.ImageField(verbose_name='Kategori Resmi')
    logo_img = models.ImageField(verbose_name='Küçük resim',null=True,blank=True)
    slug = models.SlugField(verbose_name='link',max_length=500,unique=True)
    main = models.ForeignKey('self', blank=True, null=True, related_name='child', on_delete=models.CASCADE)
    active = models.BooleanField(verbose_name='Yayın',default=True)
    video = models.CharField(verbose_name='Video linki', max_length=5000)
    title = models.CharField(verbose_name='Başlık', max_length=200)
    meta_desc = models.CharField(verbose_name='Meta Açıklaması', max_length=200)


    def __str__(self):
        return self.name

    def get_active(self):
        if self.active:
            return 'Aktif'
        else:
            return 'Pasif'





class Product(models.Model):
    name = models.CharField(verbose_name='Ürün Adı', max_length=200)
    category = models.ForeignKey(Category, verbose_name='Kategori', on_delete=models.CASCADE)
    sale_price = models.FloatField(verbose_name='Piyasa Fiaytı', max_length=200)
    discount_price = models.FloatField(verbose_name='Satış Fiyatı', max_length=200)
    #pincode = models.ManyToManyField(PinCode,null=True,blank=True)
    stock = models.IntegerField(verbose_name='Stok', max_length=200)
    productimg = models.ImageField(verbose_name='Ürün resmi')
    main = models.ForeignKey('self', blank=True, null=True, related_name='child', on_delete=models.CASCADE)
    active = models.BooleanField(verbose_name='Yayın', default=True)
    
    def __str__(self):
        return self.name
    def get_active(self):
        if self.stock <= 5:
            return False

    def rate(self):
        minuse = self.sale_price-self.discount_price
        return (100*minuse)/self.sale_price
    def get_stock(self):
        if self.stock < 5:
            return 'Stok Yok'
        else:
            return 'Stokta'


class DiscountProduct(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)    

class NewProduct(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)  
   

class Slider(models.Model):
    slider = models.ImageField(verbose_name='Slide')

class Commerce(models.Model):
    commerce_img=models.ImageField(verbose_name='Ara Reklam')
    url = models.CharField(verbose_name='Yönlendirme Linki',max_length=255)


class PinCode(models.Model):
    pin_code=models.CharField(verbose_name='Pin Kodu',max_length=255,default='Kodunuz Tedairk Aşamasındadır.')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    
