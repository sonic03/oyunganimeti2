from django import forms
from django.forms import fields
from products.models import PinCode


class LoginForm(forms.Form):
    email = forms.EmailField(required=True,max_length=255,label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Parola",widget=forms.PasswordInput(attrs={'class':'form-control'}))

class PinDeliveryForm(forms.ModelForm):
    class Meta:
        model=PinCode
        fields=('pin_code',)
    