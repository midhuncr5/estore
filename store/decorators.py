from django.shortcuts import redirect
from django.contrib import messages


def signin_required(fn):

    def wrapped(request,*args,**kwargs):

        if request.user.is_authenticated:

            return fn(request,*args,**kwargs)
        
        else:

            messages.error(request,"invalid session please login")

            return redirect("login")
        
    return wrapped
            
