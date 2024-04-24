from .models import Kyc
from django.shortcuts import redirect ,get_list_or_404
from.models import User
from functools import wraps
from django.contrib.auth.decorators import login_required


def kyc_authentication(view_func):
    @wraps(view_func)
    @login_required(login_url="login")
    def wrapper_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                instance = Kyc.objects.get(user=request.user)
                return view_func(request,instance=instance,*args ,**kwargs)
            except Kyc.DoesNotExist:
                return redirect('kyc1')
    return wrapper_view
        