"""
Django settings for instagram project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# instagram_project/instagram
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# instagram_project/
ROOT_DIR = os.path.dirname(BASE_DIR)
# instagram_project/.config_secret/
CONFIG_SECRET_DIR = os.path.join(ROOT_DIR, '.config_secret')

# instagram_project/instagram/media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
# instagram_project/instagram/static/.
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
# STATIC_URL로의 요청은 STATICFILES_DIR경로의 목록에서 파일을 찾아
STATICFILES_DIRS = [
    STATIC_DIR,
]
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

AUTH_USER_MODEL = 'member.User'
LOGIN_URL = 'member:login'
# 기본 인증 벡엔드에 페이스북 인증 백엔드를 추가함
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'member.backends.FacebookBackend',
]
# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

# 1. CONFIG_SECRET_DIR내의 'settings_common.json'파일을 읽고 ,
# 그 결과를 config_secret_common_str변수에 할당
with open(os.path.join(CONFIG_SECRET_DIR, 'settings_common.json')) as f:
    config_secret_common_str = f.read()
# 2. json.loads(<json string>)함수를 호출하여
# JSON텍스트 파일의 내용을 Python dict형태로 변환,
# config_secret_common에 할당
config_secret_common_dict = dict(json.loads(config_secret_common_str))

# 3. config_secret_common_dict 변수의 django > secret_key에
# 해당하는 value를 SECRET_KEY
SECRET_KEY = config_secret_common_dict['django']['secret_key']
# 4. .gitignore에 .config_secret/ 반영

# Facebook
FACEBOOK_APP_ID = config_secret_common_dict['facebook']['app_id']
FACEBOOK_APP_SECRET_CODE = config_secret_common_dict['facebook']['secret_code']
FACEBOOK_SCOPE = [
    'user_friends',
    'public_profile',
    'email',
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "*",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'post',
    'django_extensions',
    'member',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = config_secret_common_dict['django']['databases']

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
