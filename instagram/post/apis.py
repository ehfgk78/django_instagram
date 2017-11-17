from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from member.serializers import UserSerializer
from post.models import Post
from post.serializers import PostSerializer
from utils.permissions import IsAuthorOrReadOnly


# 다중 상속의 순서 : 오른쪽 ---> 왼쪽
class PostList(generics.ListCreateAPIView):
    # generics.GenericAPIView와 mixins를 상속받아 처리
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    lookup_url_kwarg = 'post_pk'
    serializer_class = PostSerializer
    permission_classes = (
        # author가 아니면 지울 수 없도록 utils.permissions모듈에
        #     isAuthorOrReadOnly클래스 생성하고, 여기에 임포트를 하여 사용
        IsAuthorOrReadOnly,
    )


class PostLikeToggle(generics.GenericAPIView):
    queryset = Post.objects.all()
    # url패턴에서 특정 Post instance를 가져오기 위한 그룹명
    lookup_url_kwarg = 'post_pk'

    # 특정 Post가 like toggle되도록 구현
    # self.get_object()  <-- GenericAPIView에 구현되어 있음
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        # 이미 유저의 like_posts목록에 현재 post(instance)가 존재할 경우
        if user.like_posts.filter(pk=instance.pk):
            user.like_posts.remove(instance)
            like_status = False
        else:
            user.like_posts.add(instance)
            like_status = True
        data = {
            'user': UserSerializer(user).data,
            'post': PostSerializer(instance).data,
            'result': like_status,
        }
        return Response(data)

# class PostDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         post = self.get_object(pk=pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=204)

