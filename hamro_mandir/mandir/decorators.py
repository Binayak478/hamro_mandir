from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps

def admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap 