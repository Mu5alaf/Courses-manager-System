from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        if not request.user.is_admin:
            return render(request, 'denied/403.html', status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view