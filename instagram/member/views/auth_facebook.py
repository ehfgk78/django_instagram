from typing import NamedTuple
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.urls import reverse
from django.views import View

__all__ = (
    'FrontFacebookLogin',
    'facebook_login',
)

User = get_user_model()


def facebook_login(request):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    class UserInfo:
        def __init__(self, data):
            self.id = data['id']
            self.email = data.get('email', '')
            self.url_picture = data['picture']['data']['url']

    app_id = settings.FACEBOOK_APP_ID
    app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
    app_access_token = f'{app_id}|{app_secret_code}'
    code = request.GET.get('code')

    def get_access_token_info(code_value):
        # 사용자가 페이스북에 로그인하기 위한 링크에 있던 'redirect_uri' GET 파라미터와 동일한 값
        redirect_uri = '{scheme}://{host}{relative_url}'.format(
            scheme=request.scheme,
            host=request.META['HTTP_HOST'],
            relative_url=reverse('member:facebook_login'),
        )
        print('redirect_uri: ', redirect_uri)
        # 엑세스 토큰 요청의 GET파라미터 목록

        url_access_token = ' https://graph.facebook.com/v2.10/oauth/access_token'
        params_access_token = {
            'client_id': app_id,
            'redirect_uri': redirect_uri,
            'client_secret': app_secret_code,
            'code': code_value,
        }
        # 요청 후 결과를 받아옴
        response = requests.get(url_access_token, params_access_token)
        # 결과는 JSON형식의 텍스트이므로 아래와 같이 사용
        # json.loads(response.content)와 같음
        return AccessTokenInfo(**response.json())

    def get_debug_token_info(token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        params_debug_token = {
            'input_token': token,
            'access_token': app_access_token,
        }
        response = requests.get(url_debug_token, params_debug_token)
        return DebugTokenInfo(**response.json()['data'])

    # 전달받은 code값 ---> AccessTokenInfo namedtuple을 반환

    access_token_info = get_access_token_info(code)
    access_token = access_token_info.access_token

    # DebugTokenInfo 가져오기
    debug_token_info = get_debug_token_info(access_token)

    # 유저정보 가져오기
    user_info_fields = [
        'id',
        'name',
        'picture',
        'email',
    ]
    url_graph_user_info = 'https://graph.facebook.com/me'
    params_graph_user_info = {
        'fields': ','.join(user_info_fields),
        'access_token': access_token,
    }
    response = requests.get(url_graph_user_info, params_graph_user_info)
    result = response.json()
    user_info = UserInfo(data=result)

    # 페이스북으로 가입한 유저의 username 형식 :  fb_<facebook_user_id>
    username = f'fb_{user_info.id}'
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_user(
            user_type=User.USER_TYPE_FACEBOOK,
            username=username,
            age=0
        )
    django_login(request, user)
    return redirect('post:post_list')


class FrontFacebookLogin(View):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    class UserInfo:
        def __init__(self, data):
            self.id = data['id']
            self.email = data.get('email', '')
            self.url_picture = data['picture']['data']['url']

    def get(self, request):
        app_id = settings.FACEBOOK_APP_ID
        app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
        app_access_token = f'{app_id}|{app_secret_code}'
        code = request.GET.get('code')

        def get_access_token_info(code_value):
            # 사용자가 페이스북에 로그인하기 위한 링크에 있던 'redirect_uri' GET 파라미터와 동일한 값
            redirect_uri = '{scheme}://{host}{relative_url}'.format(
                scheme=request.scheme,
                host=request.META['HTTP_HOST'],
                redirect_url=reverse('member:facebook_login'),
            )
            print('redirect_uri: ', redirect_uri)
            # 엑세스 토큰 요청의 GET파라미터 목록
            url_access_token = ' https://graph.facebook.com/v2.10/oauth/access_token'
            params_access_token = {
                'client_id': app_id,
                'redirect_uri': redirect_uri,
                'client_secret': app_secret_code,
                'code': code_value,
            }
            # 요청 후 결과를 받아옴
            response = requests.get(url_access_token, params_access_token)
            # 결과는 JSON형식의 텍스트이므로 아래와 같이 사용
            # json.loads(response.content)와 같음
            return self.AccessTokenInfo(**response.json())

        def get_debug_token_info(token):
            url_debug_token = 'https://graph.facebook.com/debug_token'
            params_debug_token = {
                'input_token': token,
                'access_token': app_access_token,
            }
            response = requests.get(url_debug_token, params_debug_token)
            return self.DebugTokenInfo(**response.json()['data'])

        # 전달받은 code값 ---> AccessTokenInfo namedtuple을 반환
        access_token_info = get_access_token_info(code)
        access_token = access_token_info.access_token
        # DebugTokenInfo 가져오기
        debug_token_info = get_debug_token_info(access_token)

        # 유저정보 가져오기
        user_info_fields = [
            'id',
            'name',
            'picture',
            'email',
        ]
        url_graph_user_info = 'https://graph.facebook.com/me'
        params_graph_user_info = {
            'fields': ','.join(user_info_fields),
            'access_token': access_token,
        }
        response = requests.get(url_graph_user_info, params_graph_user_info)
        result = response.json()
        user_info = self.UserInfo(data=result)

        data = {
            'facebook_user_id': user_info.id,
            'access_token': access_token,
        }
        return JsonResponse(data)
