from datetime import timedelta
from typing import Any
from django.utils import timezone
from django.contrib.auth import logout
from functools import wraps
from django.shortcuts import redirect



def check_session(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        last_activity =request.session.get('last_activity')
        if last_activity is None or (timezone.now() - last_activity) > timedelta(seconds=12):
            return redirect('login')

        request.session['last_activity'] =timezone.now()

        return func(request, *args, **kwargs)
    return wrapper
        