from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserSerializer, SignupSerializer

User = get_user_model()

class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        # 전달받은 username, password값으로 authenticate실행
        user = authenticate(
            username=username,
            password=password,
        )
        # user가 존재할 경우 (authenticate성공)
        if user:
            # 'user'키에 다른 dict로 user에 대한 모든 정보를 보내줌
            token, token_created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user': UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_200_OK)
        # 인증에 실패한 경우

        data = {
            'message': 'Invalid credentials'
        }
        return Response(data)
        # request.data를 사용
        # 1. username/password를 받음
        # 2. authenticate를 이용해 사용자 인증
        # 3. 인증된 사용자에 해당하는 토큰 생성
        # 4. 사용자 정보와 token.key값을 response


class Signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # print("test= ", request.data)
        # # 회원가입 후 토큰 생성, 유저정보 및 토큰 키 반환
        # username = request.data['username']
        # password = request.data['password']
        # age=request.data['age']
        #
        # if User.objects.filter(username=username).exists():
        #     return Response({'message': 'Username already exist'})
        # user = User.objects.create_user(
        #     username=username,
        #     password=password,
        #     age=age,
        # )
        # token = Token.objects.create(user=user)
        # data = {
        #     'token': token.key,
        #     'user': UserSerializer(user).data,
        # }
        # return Response(data, status=status.HTTP_200_OK)
