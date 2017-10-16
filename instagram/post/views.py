from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
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
        'posts' : posts,
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
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
    elif request.method == 'GET':
        return render(request, 'post/post_create.html')



def add_comment(request):
    # if request.method == 'POST':
    #     comment = request.POST.get('comment')
    #     if comment:
    #         add_comment = PostComment.objects.create(
    #             content=comment)
    #         context={
    #             'comment': add_comment,
    #         }
    #     else:
    #         context={}
    return render(request, 'post/post_list.html', {})


def comment_delete(request, pk):
    if request.method == 'POST':
        comment = PostComment.objects.get(pk=pk)
        comment.delete()
        return redirect('post_list')
    return HttpResponse('Permission denied', status=403)