from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .form import PostForm, CommentForm
from .models import Post, PostComment


def post_list(request):
    """
    모든 Post목록을 리턴
    template은 'post/post_list.html'을 사용
    :param request:
    :return:
    """
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    """
    Post생성
    반드시 photo필드에 해당하는 파일이 와야한다.
    :param request:
    :return:
    1. post_create.html파일을 만들고
      /post/create/ URL로 요청이 온 경우
      이 view에서 해당 파일을 render하여 reponse
    2. post_create.html에 form을 만들고,
      file input과 button요소를 배치
      file input의 name은 'photo'로 지정
    3. 이 뷰에서 request.method가 'POST'일 경우,
      requeset.POST와 request.FILES를 print문으로 출력
      'GET'이면 템플릿 파일을 보여주는 로직을 그대로 실행
    """
    # if request.method == 'POST'and request.FILES.get('photo'):
    #     # print(request.POST)
    #     # print(request.FILES)
    #
    #     #1. 파일이 오지 않았을 경우, GET요청과 같은 결가를 리턴
    #     #  1-1. 단, return render(...) 방식으로 같은 함수를 두번 호출하지 말것
    #     photo = request.FILES['photo']
    #     post = Post.objects.create(photo=photo)
    #     return HttpResponse(f'<img src="{post.photo.url}">')
    # return render(request, 'post/post_create.html')

    # Using FormField
    if request.method == 'POST':
        # POST요청의 경우 Post인스턴스를 생성하면 request.POST, request.FILES를 사용
        form = PostForm(request.POST, request.FILES)
        # form 생성과정에서 전달된 데이터들이 Form의 모든 Field들에 유효한지 검사
        if form.is_valid():
            # 유효할 경우 Post인스턴스를 생성 및 저장
            print(form.cleaned_data)
            post = Post.objects.create(
                photo=form.cleaned_data['photo']
            )
            return HttpResponse(f'<img src="{post.photo.url}">')
        else:
            # Get요청의 경우, 빈 PostForm인스턴스를 생성해서 템플릿에 전달
            form = PostForm()
        # GET요청에선 이 부분이 무조건 실행
        # POST요청에선 form.is_valid()를 통과하지 못하면 이부분이 실행
        context = {
            'form': form,
        }
        # return HttpResponse('Form invalid')
        # else:
        return render(request, 'post/post_create.html', context)


def post_detail(request, post_pk):
    # 해당 post의 사진을 img태그로 출력
    # post = Post.objects.get(pk=post_pk)
    post = get_object_or_404(Post, pk=post_pk)
    context = {
        'post': post,
    }
    return render(request, 'post/post_detail.html', context)


def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            comment = PostComment.objects.create(
                post=post,
                content=form.cleaned_data['content']
            )
            # return HttpResponse(f'''
            # <p> {comment.content} </p>
            # <p> {comment.created_at} </p>
            # ''')
            next = request.GET.get('next')
            if next:
                return redirect()
            return redirect('post_detail', post_pk=post.pk)
        else:
            post = get_object_or_404(Post, pk=post_pk)
            comment_form = CommentForm()
        context = {
            'post': post,
            'comment_form': comment_form,
        }
    return render(request, 'post/add_comment.html', context)


def comment_delete(request, pk):
    if request.method == 'POST':
        comment = PostComment.objects.get(pk=pk)
        comment.delete()
        return redirect('post_list')
    return HttpResponse('Permission denied', status=403)
