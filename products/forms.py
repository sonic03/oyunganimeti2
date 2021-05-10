from django import VERSION, forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.base import Model
from django.forms import TextInput, fields
from django.forms.widgets import Widget
from management.models import MyUser

from .models import Category, Commerce,Product,Slider



class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'desc', 'cat_img', 'slug', 'main', 'active', 'logo_img','video','title','meta_desc','summary')
        widgets ={
            'name':TextInput(attrs={'class':'form-control'}),
            'desc':forms.Textarea(attrs={'class':'form-control'}),
            'summary':TextInput(attrs={'class':'form-control'}),
            'slug':TextInput(attrs={'class':'form-control'}),
            'main' : forms.Select(attrs={'class': 'form-control'}),
            'active':forms.CheckboxInput(),
            'video':TextInput(attrs={'class':'form-control'}),
            'title':TextInput(attrs={'class':'form-control'}),
            'meta_desc':TextInput(attrs={'class':'form-control'}),

        }


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'sale_price', 'discount_price', 'active', 'stock', 'productimg', 'category', 'main','most_seller','discounted','news')
        widgets ={
            'name':TextInput(attrs={'class':'form-control'}),
            'sale_price':TextInput(attrs={'class':'form-control'}),
            'discount_price': TextInput(attrs={'class':'form-control'}),
            'stock': TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class': 'form-control'}),
            'main' : forms.Select(attrs={'class': 'form-control'}),
            'active':forms.CheckboxInput(),
            'most_seller':forms.CheckboxInput(),
            'discounted':forms.CheckboxInput(),
            'news':forms.CheckboxInput(),
            

        }

class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ('slider',)

class CommerceForm(forms.ModelForm):
    class Meta:
        model = Commerce
        fields = ('commerce_img','url')


class LoginSiteForm(forms.Form):
    email = forms.EmailField(required=True,max_length=255,widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Parola'}))

class RegisterSiteForm(forms.Form):
    email = forms.EmailField(required=True,max_length=255,widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Parola'}))
    repassword = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Parolayı Tekrar Yazın'}))
    is_accept = forms.BooleanField(required=True,label="Kabul ediyorum")

    def clean(self):
        password=self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')
        email = self.cleaned_data.get('email')
        is_accept =  self.cleaned_data.get("is_accept")
        if password and repassword and password != repassword:
            raise forms.ValidationError("Şifreler uyuşmuyor. Tekrar deneyiniz.")
        if not "@" in email:
            raise forms.ValidationError("Eposta formatı halatı")
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu kullanıcı sitemizde kayıtlıdır.")
        if not is_accept:
            raise forms.ValidationError("Üyelik sözleşmesini kabul etmeden üye olamazsınız")
        return self.cleaned_data
        