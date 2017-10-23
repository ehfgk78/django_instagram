from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from post.decorators import login_required
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


@login_required
def post_create(request):
    if not request.user.is_authenticated:
        return redirect('member:login')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Post.objects.create(
            #     photo=form.cleaned_data['photo'],
            #     author=request.user,
            # )
            # 기존 Django의 ModelForm방식 사용
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:post_list')
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_detail(request, post_pk):
    if not request.user.is_authenticated:
        return redirect('member:login')
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


def post_delete(request, post_pk):
    if not request.user.is_authenticated:
        return redirect('member:login')
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        if post.author == request.user:
            post.delete()
            return redirect('post:post_list')
        else:
            raise PermissionDenied('작성자가 아닙니다 ')


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
            next_path = request.GET.get('next', '').strip()
            # 다음에 갈 URL (next)가 빈 문자열이 아닌 경우
            if next_path:
                return redirect(next_path)
            # 지정되지 않으면 post_detail로 이동
            return redirect('post:post_detail', post_pk=post_pk)


def comment_delete(request, comment_pk):
    next_path = request.GET.get('next', '').strip()
    if request.method == 'POST':
        comment = get_object_or_404(PostComment, pk=comment_pk)
        if comment.author == request.user:
            comment.delete()
            if next_path:
                return redirect(next_path)
            return redirect('post:post_detail', post_pk=comment.post.pk)
        else:
            raise PermissionDenied('작성자가 아닙니다.')


# @login_required
def post_like_toggle(request, post_pk):
    """
    post_pk에 해당하는 Post가  현재 로그인한 유저의 like_posts에
       있다면  없애고
       없다면 추가
    post.html에서 현재 user가 해당 post를 like했는지 표시
    :param request:
    :param post_pk:
    :return:
    """
    if request.method == 'POST':
        # GET 파라미터로 전달될 때 URL
        next_path = request.GET.get('next')

        # post_pk에 해당하는 Post객체
        post = get_object_or_404(Post, pk=post_pk)

        # 요청한 사용자
        user = request.user

        # 사용자의 like_posts목록에서 like_toggle할 Post가 있는지 확인
        filtered_like_posts = user.like_posts.filter(pk=post.pk)

        # 존재할 경우, like_posts목록에서 해당 Post 삭제
        if filtered_like_posts.exists():
            user.like_posts.remove(post)

        # 없을 경우, like_posts목록에서 해당 Post 추가
        else:
            user.like_posts.add(post)

        # 이동할 path가 존재할 경우 해당 위치로, 없을 경우 Post 상세페이지로 이동
        if next_path:
            return redirect(next_path)
        return redirect('post:post_detail', post_pk=post_pk)
