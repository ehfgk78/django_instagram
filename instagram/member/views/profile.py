from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

__all__ = (
    'profile',
)


@login_required
def profile(request):
    return HttpResponse(f'User profile page { request.user }')
