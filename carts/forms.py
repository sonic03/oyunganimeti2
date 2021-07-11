from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError

class TelForm(forms.Form):
    tel = forms.CharField(required=True,max_length=11,label='Telefon Numarası',widget=forms.NumberInput(attrs={'class':'form-control'}))

class KKForm(forms.Form):
    isim = forms.CharField(required=True,max_length=255,label='Kart Sahibi',widget=forms.TextInput(attrs={'class':'contact-items','placeholder':'Kart Sahibi'}))
    kkno = forms.CharField(required=True,max_length=16,label='Kredi Kartı Numarası',widget=forms.NumberInput(attrs={'class':'contact-items','placeholder':'Kredi Kartı Numarası'}))
    skay = forms.CharField(required=True,max_length=2,label='Ay',widget=forms.NumberInput(attrs={'class':'contact-items','placeholder':'Ay'}))
    skyil = forms.CharField(required=True,max_length=2,label='Yıl',widget=forms.NumberInput(attrs={'class':'contact-items','placeholder':'Yıl'}))
    cvc = forms.CharField(required=True,max_length=3,label='cvc',widget=forms.NumberInput(attrs={'class':'contact-items','placeholder':'CVC'}))
    gsm = forms.CharField(required=True,max_length=11,label='Telefon Numarası',widget=forms.NumberInput(attrs={'class':'contact-items','placeholder':'Telefon Numarası'}))

    def clean(self):
        isim=self.cleaned_data.get("isim")
        kkno=self.cleaned_data.get("kkno")
        skay=self.cleaned_data.get("skay")
        skyil=self.cleaned_data.get("skyil")
        cvc=self.cleaned_data.get("cvc")
        gsm=self.cleaned_data.get("gsm")

        if not isim:
            raise ValidationError("İsim alanı boş kalamaz")
        if kkno and len(kkno) != 16:
            raise ValidationError("Lütfen 16 haneli kredi kartı numaranızı giriniz")