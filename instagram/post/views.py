from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm
from .models import Post, PostComment

User = get_user_model()


def post_list(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    if not request.user.is_authenticated:
        return redirect('member:login')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(
                photo=form.cleaned_data['photo'],
                author=request.user,
            )
            return redirect('post:post_list')
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


def post_delete(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        if post.author == request.user:
            post.delete()
            return redirect('post:post_list')
        else:
            raise PermissionDenied


def comment_create(request, post_pk):
    if not request.user.is_authenticated:
        return redirect('member:login')

    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            PostComment.objects.create(
                post=post,
                content=form.cleaned_data['content'],
                author=request.user,
            )
            # GET parameter로 'next'값이 전달되면
            # 공백을 없애고 다음에 redirect될 주소로 지정
            next = request.GET.get('next', '').strip()
            # 다음에 갈 URL (next)가 빈 문자열이 아닌 경우
            if next:
                return redirect(next)
            # 지정되지 않으면 post_detail로 이동
            return redirect('post:post_detail', post_pk=post_pk)


def comment_delete(request, comment_pk):
    comment = PostComment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('post:post_list')
