from django.shortcuts import redirect


def to_post_list(request):
    return redirect('post:post_list')