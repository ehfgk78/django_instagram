from urllib.parse import urlparse

from django.shortcuts import redirect
from django.urls import reverse


def login_required(view_func):
    def wrapper_view_func(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated:
            referer = urlparse(request.META['HTTP_REFERER']).path
            url = '{base_url}?next={referer}'.format(
                base_url=reverse('member:login'),
                referer= referer)
            return redirect(url)
            return redirect('member:login')
        return view_func(*args, **kwargs)
    return wrapper_view_func
