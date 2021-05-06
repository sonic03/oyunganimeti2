from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect

def is_login_and_admin(func):
    def wrapper(request,*args, **kwargs):
        if request.user.is_authenticated:
            if request.user.admin:
               return func(request,*args, **kwargs)
            return redirect('management:adminlogin')
        return redirect('management:adminlogin')
    return wrapper

def not_authenticate(func):
    def wrapper(request,*args, **kwargs):
        if not request.user.is_authenticated:
            return func(request,*args, **kwargs)
    return wrapper