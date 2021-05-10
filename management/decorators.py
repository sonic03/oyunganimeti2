from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect,render
from core.models import Repeary

def is_login_and_admin(func):
    def wrapper(request,*args, **kwargs):
        if request.user.is_authenticated and request.user.admin:
            return func(request,*args, **kwargs)
        else:
            return redirect("index")
       
    return wrapper

def not_authenticate(func):
    def wrapper(request,*args, **kwargs):
        if not request.user.is_authenticated:
            return func(request,*args, **kwargs)
    return wrapper

def bakim(func):
    def wrapper(request,*args, **kwargs):
        if not settings.REPAIR_MODE:
            return func(request,*args, **kwargs)
        else:
            return redirect("bakim")
    return wrapper

