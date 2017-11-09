from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from post.models import Post
from post.serializers import PostSerializer


class PostList(APIView):
    # generics.GenericAPIView와 mixins를 상속받아 처리
    # api/post
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # 이 과정에서 author값을 request.user로 채우기
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


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
